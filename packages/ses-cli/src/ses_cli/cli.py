from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from ses_cli import __version__
from ses_cli.check_cmd import run_check
from ses_cli.init_cmd import run_init
from ses_cli.questionnaire import answers_from_flags, interactive_answers
from ses_cli.setup_cmd import run_setup

app = typer.Typer(
    name="ses",
    help="Solo Engineering System — init, setup, and local checks (no GitHub Actions).",
    no_args_is_help=True,
)


@app.callback()
def main() -> None:
    """SES CLI."""


@app.command("version")
def version_cmd() -> None:
    """Print CLI version."""
    typer.echo(__version__)


def _resolve_answers(
    *,
    name: Optional[str],
    purpose: Optional[str],
    languages: Optional[str],
    api: Optional[bool],
    ui: Optional[bool],
    db: Optional[bool],
    risk: Optional[str],
    sensitive: Optional[str],
    yes: bool,
):
    if yes:
        missing = [
            label
            for label, val in [
                ("--name", name),
                ("--purpose", purpose),
                ("--languages", languages),
                ("--api/--no-api", api),
                ("--ui/--no-ui", ui),
                ("--db/--no-db", db),
                ("--risk", risk),
            ]
            if val is None
        ]
        if missing:
            typer.secho(
                "Non-interactive init requires: " + ", ".join(missing),
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(code=1)
        sens_list = [s.strip() for s in (sensitive or "none").split(",")]
        return answers_from_flags(
            name=name or "",
            purpose=purpose or "",
            languages=languages or "",
            api=bool(api),
            ui=bool(ui),
            db=bool(db),
            risk=risk or "",
            sensitive=sens_list,
        )

    if any(v is not None for v in (name, purpose, languages, api, ui, db, risk, sensitive)):
        n = name or typer.prompt("Product name (slug)").strip()
        p = purpose or typer.prompt("One-line purpose").strip()
        langs = (
            languages
            or typer.prompt("Languages [python/typescript/both]", default="python")
        ).strip()
        has_api = (
            api if api is not None else typer.confirm("Has a documented HTTP API?", default=False)
        )
        has_ui = ui if ui is not None else typer.confirm("Has a web UI?", default=False)
        has_db = db if db is not None else typer.confirm("Needs a database?", default=False)
        r = (
            risk or typer.prompt("Risk posture [side-project/commercial]", default="side-project")
        ).strip()
        sens_raw = sensitive or typer.prompt("Sensitive domains (comma)", default="none")
        return answers_from_flags(
            name=n,
            purpose=p,
            languages=langs,
            api=has_api,
            ui=has_ui,
            db=has_db,
            risk=r,
            sensitive=[s.strip() for s in sens_raw.split(",")],
        )

    return interactive_answers()


@app.command("init")
def init_cmd(
    name: Optional[str] = typer.Option(None, "--name", help="Product slug"),
    purpose: Optional[str] = typer.Option(None, "--purpose", help="One-line purpose"),
    languages: Optional[str] = typer.Option(
        None, "--languages", help="python | typescript | both"
    ),
    api: Optional[bool] = typer.Option(None, "--api/--no-api", help="HTTP API module"),
    ui: Optional[bool] = typer.Option(None, "--ui/--no-ui", help="Web UI module"),
    db: Optional[bool] = typer.Option(None, "--db/--no-db", help="SQLite database module"),
    risk: Optional[str] = typer.Option(None, "--risk", help="side-project | commercial"),
    sensitive: Optional[str] = typer.Option(
        None,
        "--sensitive",
        help="Comma-separated: auth,payments,pii,none",
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Non-interactive: require flag answers (no prompts)",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Wipe cwd contents except .git, then scaffold (destructive)",
    ),
    check: bool = typer.Option(
        False,
        "--check/--no-check",
        help="Run ses check after init (install product deps first)",
    ),
    path: Optional[Path] = typer.Option(
        None,
        "--path",
        help="Target directory (default: cwd)",
        file_okay=False,
    ),
    skeleton: Optional[Path] = typer.Option(
        None, "--skeleton", help="Path to skeleton/ directory", exists=True, file_okay=False
    ),
) -> None:
    """Scaffold a product into the current directory (or --path)."""
    answers = _resolve_answers(
        name=name,
        purpose=purpose,
        languages=languages,
        api=api,
        ui=ui,
        db=db,
        risk=risk,
        sensitive=sensitive,
        yes=yes,
    )
    run_init(
        answers,
        force=force,
        skeleton_path=skeleton,
        dest=path,
        run_check=check,
    )


@app.command("setup")
def setup_cmd(
    docs: bool = typer.Option(
        False,
        "--docs",
        help="Also write/refresh .ses/standards/ from the installed kit",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Overwrite existing SES-managed Cursor files",
    ),
    path: Optional[Path] = typer.Option(
        None,
        "--path",
        help="Target directory (default: cwd)",
        file_okay=False,
        exists=True,
    ),
) -> None:
    """Materialize Cursor rules/skills (and optional standards) into a product repo."""
    run_setup(target=path, docs=docs, force=force)


@app.command("check")
def check_cmd(
    path: Optional[Path] = typer.Option(
        None,
        "--path",
        help="Product directory containing ses.toml (default: walk from cwd)",
        file_okay=False,
        exists=True,
    ),
) -> None:
    """Run local checks for a product (pass / fail / not configured)."""
    code = run_check(path=path)
    raise typer.Exit(code)


if __name__ == "__main__":
    app()
