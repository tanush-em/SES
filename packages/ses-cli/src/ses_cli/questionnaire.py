from __future__ import annotations

import typer

from ses_cli.models import (
    VALID_LANGUAGES,
    VALID_RISKS,
    VALID_SENSITIVE,
    InitAnswers,
)


def _prompt_choice(label: str, choices: tuple[str, ...], default: str) -> str:
    shown = "/".join(choices)
    value = typer.prompt(f"{label} [{shown}]", default=default)
    value = value.strip().lower()
    if value not in choices:
        raise typer.BadParameter(f"Expected one of {choices}, got {value!r}")
    return value


def _prompt_yes_no(label: str, default: bool) -> bool:
    return typer.confirm(label, default=default)


def _prompt_sensitive() -> list[str]:
    raw = typer.prompt(
        "Likely sensitive domains? (comma: auth,payments,pii,none)",
        default="none",
    )
    items = [p.strip().lower() for p in raw.split(",") if p.strip()]
    if not items:
        items = ["none"]
    for item in items:
        if item not in VALID_SENSITIVE:
            raise typer.BadParameter(f"Invalid sensitive domain {item!r}")
    if "none" in items and len(items) > 1:
        items = [i for i in items if i != "none"]
    return items


def interactive_answers() -> InitAnswers:
    name = typer.prompt("Product name (slug)").strip()
    purpose = typer.prompt("One-line purpose").strip()
    languages = _prompt_choice("Languages", VALID_LANGUAGES, "python")
    has_api = _prompt_yes_no("Has a documented HTTP API?", default=False)
    has_ui = _prompt_yes_no("Has a web UI?", default=False)
    has_db = _prompt_yes_no("Needs a database?", default=False)
    if has_db:
        typer.echo("Database default: SQLite. Graduate to Postgres when concurrent writers/ops need it.")
    risk = _prompt_choice("Risk posture", VALID_RISKS, "side-project")
    sensitive = _prompt_sensitive()
    answers = InitAnswers(
        name=name,
        purpose=purpose,
        languages=languages,
        has_api=has_api,
        has_ui=has_ui,
        has_db=has_db,
        risk=risk,
        sensitive=sensitive,
    )
    answers.validate()
    return answers


def answers_from_flags(
    *,
    name: str,
    purpose: str,
    languages: str,
    api: bool,
    ui: bool,
    db: bool,
    risk: str,
    sensitive: list[str],
) -> InitAnswers:
    items = [s.strip().lower() for s in sensitive if s.strip()]
    if not items:
        items = ["none"]
    if "none" in items and len(items) > 1:
        items = [i for i in items if i != "none"]
    answers = InitAnswers(
        name=name.strip(),
        purpose=purpose.strip(),
        languages=languages.strip().lower(),
        has_api=api,
        has_ui=ui,
        has_db=db,
        risk=risk.strip().lower(),
        sensitive=items,
    )
    answers.validate()
    return answers
