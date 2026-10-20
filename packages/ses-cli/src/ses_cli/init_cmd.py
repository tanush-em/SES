from __future__ import annotations

import shutil
from pathlib import Path

import typer

from ses_cli.models import InitAnswers
from ses_cli.paths import cwd_is_scaffoldable, ensure_ses_gitignore, resolve_kit_roots
from ses_cli.setup_cmd import run_setup
from ses_cli.skeleton import copy_tree


def _module_copy_roots(mod: str, answers: InitAnswers, mod_dir: Path) -> list[Path]:
    """Return directories to copy for a module (handles multi-runtime overlays)."""
    if mod != "db-sqlite":
        return [mod_dir]
    roots: list[Path] = []
    if answers.has_python and (mod_dir / "backend").is_dir():
        roots.append(mod_dir / "backend")
    if answers.has_lib and (mod_dir / "lib").is_dir():
        roots.append(mod_dir / "lib")
    if answers.has_ts_api and (mod_dir / "server").is_dir():
        roots.append(mod_dir / "server")
    return roots


def _clear_dest(dest: Path) -> None:
    """Remove all contents except .git."""
    for path in list(dest.iterdir()):
        if path.name == ".git":
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


def run_init(
    answers: InitAnswers,
    *,
    force: bool = False,
    skeleton_path: Path | None = None,
    dest: Path | None = None,
    run_check: bool = False,
    run_setup_step: bool = True,
) -> Path:
    answers.validate()
    target = (dest or Path.cwd()).resolve()

    try:
        kit = resolve_kit_roots(skeleton=skeleton_path)
    except FileNotFoundError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    ok, reason = cwd_is_scaffoldable(target, force=force)
    if not ok:
        typer.secho(reason, fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    target.mkdir(parents=True, exist_ok=True)
    if force:
        _clear_dest(target)

    skel = kit.skeleton
    context = answers.template_context()
    pkg = answers.python_package

    try:
        copy_tree(skel / "base", target, context, package_name=pkg)

        for mod in answers.modules():
            mod_dir = skel / "modules" / mod
            if not mod_dir.is_dir():
                raise FileNotFoundError(f"Module skeleton missing: {mod_dir}")
            for src in _module_copy_roots(mod, answers, mod_dir):
                if mod == "db-sqlite":
                    copy_tree(src, target / src.name, context, package_name=pkg)
                else:
                    copy_tree(src, target, context, package_name=pkg)

        env_path = target / ".env"
        if env_path.exists():
            env_path.unlink()

        ensure_ses_gitignore(target)

    except Exception as exc:
        typer.secho(f"ses init failed: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    typer.secho(f"Scaffolded product in {target}", fg=typer.colors.GREEN)
    typer.echo("Modules: " + ", ".join(answers.modules()))

    if run_setup_step:
        typer.echo("")
        run_setup(target=target, docs=False, force=True, kit=kit)

    typer.echo("")
    typer.echo("Next:")
    if answers.has_python:
        typer.echo("  cd backend && python -m venv .venv && source .venv/bin/activate")
        typer.echo('  pip install -e ".[dev]"')
    if answers.has_ui:
        typer.echo("  cd web && npm install")
    if answers.has_lib:
        typer.echo("  cd lib && npm install")
    if answers.has_ts_api:
        typer.echo("  cd server && npm install")
    typer.echo("  ses check")

    if run_check:
        from ses_cli.check_cmd import run_check as do_check

        typer.echo("")
        typer.echo("Running smoke ses check...")
        code = do_check(path=target)
        if code != 0:
            typer.secho(
                f"Smoke check exited {code}. Product was created; fix deps/checks and re-run.",
                fg=typer.colors.YELLOW,
                err=True,
            )
            raise typer.Exit(code=code)

    return target
