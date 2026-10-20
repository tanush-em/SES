from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class KitRoots:
    """Resolved locations for skeleton, standards, and product Cursor templates."""

    skeleton: Path
    standards: Path
    product_cursor: Path
    source: str  # "package-data" | "monorepo" | "explicit"


def find_repo_root(start: Path | None = None) -> Path | None:
    """Walk up looking for kit markers: skeleton/ + standards/."""
    here = start.resolve() if start is not None else Path(__file__).resolve().parent
    for candidate in [here, *here.parents]:
        if (candidate / "skeleton").is_dir() and (candidate / "standards").is_dir():
            return candidate
    return None


def package_data_root() -> Path:
    return Path(__file__).resolve().parent / "data"


def resolve_kit_roots(
    *,
    skeleton: Path | None = None,
    start: Path | None = None,
) -> KitRoots:
    """Prefer monorepo checkout when developing; else vendored package data."""
    if skeleton is not None:
        skel = skeleton.resolve()
        # Infer sibling standards/templates from skeleton parent when possible
        parent = skel.parent
        standards = parent / "standards"
        product_cursor = parent / "templates" / "product-cursor"
        if not standards.is_dir() or not product_cursor.is_dir():
            data = package_data_root()
            standards = data / "standards" if (data / "standards").is_dir() else standards
            product_cursor = (
                data / "product-cursor"
                if (data / "product-cursor").is_dir()
                else product_cursor
            )
        return KitRoots(
            skeleton=skel,
            standards=standards,
            product_cursor=product_cursor,
            source="explicit",
        )

    repo = find_repo_root(start)
    if repo is not None:
        return KitRoots(
            skeleton=repo / "skeleton",
            standards=repo / "standards",
            product_cursor=repo / "templates" / "product-cursor",
            source="monorepo",
        )

    data = package_data_root()
    skel = data / "skeleton"
    standards = data / "standards"
    product_cursor = data / "product-cursor"
    if skel.is_dir() and standards.is_dir() and product_cursor.is_dir():
        return KitRoots(
            skeleton=skel,
            standards=standards,
            product_cursor=product_cursor,
            source="package-data",
        )

    raise FileNotFoundError(
        "Could not locate SES kit data (skeleton/standards/templates). "
        "Install ses-cli with package data, run from the SES kit repo, or pass --skeleton."
    )


SES_GITIGNORE_LINES = [
    "# SES regenerable (restore with: ses setup)",
    ".cursor/rules/ses-*.mdc",
    ".cursor/skills/feature-planning/",
    ".cursor/skills/feature-implementation/",
    ".cursor/skills/independent-review/",
    ".ses/",
]


def ensure_ses_gitignore(dest: Path) -> None:
    """Append SES regenerable paths to .gitignore if missing."""
    gitignore = dest / ".gitignore"
    existing = gitignore.read_text(encoding="utf-8") if gitignore.is_file() else ""
    to_add: list[str] = []
    for line in SES_GITIGNORE_LINES:
        if line.startswith("#"):
            # add comment only when we add at least one path
            continue
        if line not in existing:
            to_add.append(line)
    if not to_add:
        return
    block = "\n".join(["", "# SES regenerable (restore with: ses setup)", *to_add, ""])
    if existing and not existing.endswith("\n"):
        existing += "\n"
    gitignore.write_text(existing + block, encoding="utf-8")


def cwd_is_scaffoldable(dest: Path, *, force: bool) -> tuple[bool, str]:
    """Return (ok, reason). Allow empty dirs or dirs that only contain .git."""
    if not dest.exists():
        return True, ""
    if not dest.is_dir():
        return False, f"Not a directory: {dest}"
    entries = [p for p in dest.iterdir() if p.name != ".git"]
    if not entries:
        return True, ""
    if force:
        return True, ""
    names = ", ".join(sorted(p.name for p in entries)[:8])
    more = "…" if len(entries) > 8 else ""
    return (
        False,
        f"Directory is not empty ({names}{more}). Pass --force to overwrite, or use an empty directory.",
    )
