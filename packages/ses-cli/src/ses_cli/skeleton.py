from __future__ import annotations

import shutil
from pathlib import Path

from jinja2 import Environment, StrictUndefined

from ses_cli.paths import find_repo_root, resolve_kit_roots

__all__ = [
    "find_repo_root",
    "skeleton_root",
    "copy_tree",
    "render_string",
]


def skeleton_root(explicit: Path | None = None) -> Path:
    roots = resolve_kit_roots(skeleton=explicit)
    if not roots.skeleton.is_dir():
        raise FileNotFoundError(f"Skeleton path not found: {roots.skeleton}")
    return roots.skeleton


def _jinja_env() -> Environment:
    return Environment(undefined=StrictUndefined, keep_trailing_newline=True)


def render_string(template: str, context: dict) -> str:
    return _jinja_env().from_string(template).render(**context)


def copy_tree(
    src: Path,
    dest: Path,
    context: dict,
    *,
    package_name: str | None = None,
) -> None:
    """Copy src into dest, rendering *.j2 and renaming __package__ dirs."""
    if not src.is_dir():
        raise FileNotFoundError(f"Skeleton path missing: {src}")

    for path in sorted(src.rglob("*")):
        rel = path.relative_to(src)
        parts: list[str] = []
        for part in rel.parts:
            if part == "__package__" and package_name:
                parts.append(package_name)
            elif part.startswith("dot-"):
                # Packaging-safe stand-in for hidden files (setuptools drops .* in wheels).
                parts.append("." + part[len("dot-") :])
            else:
                parts.append(part)
        out_rel = Path(*parts) if parts else Path()
        out_path = dest / out_rel

        if path.is_dir():
            out_path.mkdir(parents=True, exist_ok=True)
            continue

        out_path.parent.mkdir(parents=True, exist_ok=True)
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".j2" or path.name.endswith(".j2"):
            name = out_path.name
            if name.endswith(".j2"):
                out_path = out_path.with_name(name[: -len(".j2")])
            out_path.write_text(render_string(text, context), encoding="utf-8")
        else:
            shutil.copy2(path, out_path)
