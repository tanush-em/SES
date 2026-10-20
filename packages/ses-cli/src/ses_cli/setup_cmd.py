from __future__ import annotations

import shutil
from pathlib import Path

import typer

from ses_cli.paths import KitRoots, ensure_ses_gitignore, resolve_kit_roots

SES_RULE_NAMES = (
    "ses-principles.mdc",
    "ses-product.mdc",
    "ses-security.mdc",
    "ses-testing.mdc",
    "ses-docs.mdc",
)

SES_SKILL_NAMES = (
    "feature-planning",
    "feature-implementation",
    "independent-review",
)


def _copy_file(src: Path, dest: Path, *, force: bool) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and not force:
        return "skip"
    shutil.copy2(src, dest)
    return "write"


def _copy_tree(src: Path, dest: Path, *, force: bool) -> str:
    if dest.exists() and not force:
        return "skip"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    return "write"


def run_setup(
    *,
    target: Path | None = None,
    docs: bool = False,
    force: bool = False,
    kit: KitRoots | None = None,
) -> Path:
    dest = (target or Path.cwd()).resolve()
    if not dest.is_dir():
        typer.secho(f"Not a directory: {dest}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    try:
        roots = kit or resolve_kit_roots()
    except FileNotFoundError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    cursor_src = roots.product_cursor
    if not cursor_src.is_dir():
        typer.secho(
            f"Product Cursor templates missing: {cursor_src}",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)

    written: list[str] = []
    skipped: list[str] = []

    rules_src = cursor_src / "rules"
    for name in SES_RULE_NAMES:
        src = rules_src / name
        if not src.is_file():
            typer.secho(f"Missing template rule: {src}", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1)
        rel = f".cursor/rules/{name}"
        action = _copy_file(src, dest / rel, force=force)
        (written if action == "write" else skipped).append(rel)

    skills_src = cursor_src / "skills"
    for name in SES_SKILL_NAMES:
        src = skills_src / name
        if not src.is_dir():
            typer.secho(f"Missing template skill: {src}", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1)
        rel = f".cursor/skills/{name}"
        action = _copy_tree(src, dest / rel, force=force)
        (written if action == "write" else skipped).append(rel)

    if docs:
        standards_src = roots.standards
        if not standards_src.is_dir():
            typer.secho(
                f"Standards missing: {standards_src}",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(code=1)
        rel = ".ses/standards"
        # --docs always refreshes standards content
        _copy_tree(standards_src, dest / rel, force=True)
        written.append(rel)

    ensure_ses_gitignore(dest)

    typer.secho(f"ses setup — {dest} (kit: {roots.source})", fg=typer.colors.GREEN)
    if written:
        typer.echo("Wrote/refreshed:")
        for item in written:
            typer.echo(f"  {item}")
    if skipped:
        typer.echo("Skipped (exists; pass --force to overwrite):")
        for item in skipped:
            typer.echo(f"  {item}")
    typer.echo("Next: open this folder in Cursor; run `ses check` when ses.toml exists.")
    return dest
