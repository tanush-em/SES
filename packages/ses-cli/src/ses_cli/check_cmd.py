from __future__ import annotations

import re
import subprocess
from pathlib import Path

import typer

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_NOT_CONFIGURED = 2

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{8,}"),
    re.compile(r"(?i)-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
    re.compile(r"(?i)aws_secret_access_key\s*=\s*\S+"),
]

SKIP_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".woff",
    ".woff2",
    ".pdf",
    ".sqlite",
    ".db",
}


def resolve_product_dir(
    *,
    path: Path | None = None,
    cwd: Path | None = None,
) -> Path:
    if path is not None:
        resolved = path.resolve()
        if not resolved.is_dir():
            typer.secho(f"Path not found: {resolved}", fg=typer.colors.RED, err=True)
            raise typer.Exit(EXIT_FAIL)
        return resolved

    here = (cwd or Path.cwd()).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / "ses.toml").is_file():
            return candidate
    typer.secho(
        "No ses.toml found (run inside a product or pass --path).",
        fg=typer.colors.RED,
        err=True,
    )
    raise typer.Exit(EXIT_NOT_CONFIGURED)


def load_checks(product_dir: Path) -> list[dict]:
    config_path = product_dir / "ses.toml"
    if not config_path.is_file():
        return []
    data = tomllib.loads(config_path.read_text(encoding="utf-8"))
    checks = data.get("checks") or {}
    steps = checks.get("steps") or []
    if not isinstance(steps, list):
        return []
    return [s for s in steps if isinstance(s, dict)]


def _run_command(step: dict, product_dir: Path) -> tuple[bool, str]:
    name = step.get("name", "command")
    command = step.get("command")
    if not command or not isinstance(command, list):
        return False, f"{name}: missing command list"
    cwd_rel = step.get("cwd") or "."
    cwd = (product_dir / cwd_rel).resolve()
    if not cwd.is_dir():
        return False, f"{name}: cwd not found: {cwd_rel}"
    try:
        proc = subprocess.run(
            [str(c) for c in command],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        return False, f"{name}: command not found ({exc}). Install project deps first."
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()
        if len(detail) > 500:
            detail = detail[:500] + "…"
        return False, f"{name}: failed (exit {proc.returncode})" + (
            f"\n{detail}" if detail else ""
        )
    return True, f"{name}: pass"


def _secret_scan(product_dir: Path) -> tuple[bool, str]:
    hits = 0
    for path in product_dir.rglob("*"):
        if not path.is_file():
            continue
        if any(
            part in {".venv", "node_modules", ".git", "dist", "build", ".ses"}
            for part in path.parts
        ):
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                hits += 1
                break
    if hits:
        return (
            False,
            f"secret-scan: fail ({hits} file(s) matched secret-like patterns; values not shown)",
        )
    return True, "secret-scan: pass"


def _architecture_doc(product_dir: Path) -> tuple[bool, str]:
    path = product_dir / "docs" / "architecture.md"
    if path.is_file() and path.stat().st_size > 0:
        return True, "architecture-doc: pass"
    return False, "architecture-doc: missing or empty docs/architecture.md"


def run_check(
    *,
    path: Path | None = None,
    cwd: Path | None = None,
) -> int:
    product_dir = resolve_product_dir(path=path, cwd=cwd)
    config_path = product_dir / "ses.toml"
    steps = load_checks(product_dir)
    if not steps:
        reason = (
            f"missing {config_path}"
            if not config_path.is_file()
            else f"no steps in {config_path}"
        )
        typer.secho(
            f"ses check: not configured ({reason})",
            fg=typer.colors.YELLOW,
            err=True,
        )
        return EXIT_NOT_CONFIGURED

    typer.echo(f"ses check — {product_dir}")
    failed = False
    for step in steps:
        step_type = step.get("type") or "command"
        if step_type == "secret-scan":
            ok, msg = _secret_scan(product_dir)
        elif step_type == "architecture-doc":
            ok, msg = _architecture_doc(product_dir)
        else:
            ok, msg = _run_command(step, product_dir)
        if ok:
            typer.secho(f"  ✓ {msg}", fg=typer.colors.GREEN)
        else:
            failed = True
            typer.secho(f"  ✗ {msg}", fg=typer.colors.RED, err=True)

    if failed:
        typer.secho("ses check: FAIL", fg=typer.colors.RED, err=True)
        return EXIT_FAIL
    typer.secho("ses check: PASS", fg=typer.colors.GREEN)
    return EXIT_PASS
