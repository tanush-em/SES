from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import typer

from ses_cli.check_cmd import EXIT_FAIL, EXIT_NOT_CONFIGURED, EXIT_PASS, run_check
from ses_cli.init_cmd import run_init
from ses_cli.models import InitAnswers
from ses_cli.paths import find_repo_root
from ses_cli.setup_cmd import run_setup


REPO = find_repo_root()
assert REPO is not None, "tests must run from SES kit repo"


def _minimal_answers(name: str = "demo-app") -> InitAnswers:
    return InitAnswers(
        name=name,
        purpose="Test product",
        languages="python",
        has_api=False,
        has_ui=False,
        has_db=False,
        risk="side-project",
        sensitive=["none"],
    )


def test_init_scaffolds_cwd(tmp_path: Path) -> None:
    dest = tmp_path / "app"
    dest.mkdir()
    answers = _minimal_answers()
    out = run_init(answers, dest=dest, run_check=False, force=False)
    assert out == dest.resolve()
    assert (dest / "ses.toml").is_file()
    assert (dest / ".env.example").is_file()
    assert not (dest / ".env").exists()
    assert (dest / "backend" / "pyproject.toml").is_file()
    assert (dest / "backend" / "src" / "demo_app" / "__init__.py").is_file()
    assert (dest / ".cursor" / "rules" / "ses-product.mdc").is_file()
    assert (dest / ".cursor" / "skills" / "feature-planning" / "SKILL.md").is_file()
    gitignore = (dest / ".gitignore").read_text(encoding="utf-8")
    assert ".cursor/rules/ses-*.mdc" in gitignore


def test_init_refuses_nonempty(tmp_path: Path) -> None:
    dest = tmp_path / "app"
    dest.mkdir()
    (dest / "existing.txt").write_text("nope", encoding="utf-8")
    with pytest.raises(typer.Exit) as exc:
        run_init(_minimal_answers(), dest=dest, run_check=False, force=False)
    assert exc.value.exit_code == 1


def test_init_force_overwrites(tmp_path: Path) -> None:
    dest = tmp_path / "app"
    dest.mkdir()
    (dest / "existing.txt").write_text("nope", encoding="utf-8")
    run_init(_minimal_answers(), dest=dest, run_check=False, force=True)
    assert not (dest / "existing.txt").exists()
    assert (dest / "ses.toml").is_file()


def test_setup_restores_cursor_files(tmp_path: Path) -> None:
    dest = tmp_path / "app"
    dest.mkdir()
    run_init(_minimal_answers("restore-me"), dest=dest, run_check=False)
    shutil.rmtree(dest / ".cursor")
    assert not (dest / ".cursor").exists()
    run_setup(target=dest, force=True)
    assert (dest / ".cursor" / "rules" / "ses-principles.mdc").is_file()
    assert (dest / ".cursor" / "skills" / "independent-review" / "SKILL.md").is_file()


def test_setup_docs(tmp_path: Path) -> None:
    dest = tmp_path / "app"
    dest.mkdir()
    run_setup(target=dest, docs=True, force=True)
    assert (dest / ".ses" / "standards" / "definition-of-done.md").is_file()


def test_check_exit_codes(tmp_path: Path) -> None:
    dest = tmp_path / "app"
    dest.mkdir()
    run_init(_minimal_answers("demo-check"), dest=dest, run_check=False)
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", ".[dev]"],
        cwd=dest / "backend",
        check=True,
        capture_output=True,
    )
    assert run_check(path=dest) == EXIT_PASS

    test_file = dest / "backend" / "tests" / "test_hello.py"
    test_file.write_text(
        "from demo_check import hello\n\ndef test_hello() -> None:\n    assert hello() == 'nope'\n",
        encoding="utf-8",
    )
    assert run_check(path=dest) == EXIT_FAIL

    test_file.write_text(
        "from demo_check import hello\n\ndef test_hello() -> None:\n    assert hello() == 'demo-check'\n",
        encoding="utf-8",
    )
    (dest / "ses.toml").unlink()
    assert run_check(path=dest) == EXIT_NOT_CONFIGURED


def test_answers_modules_ui_forces_typescript() -> None:
    answers = InitAnswers(
        name="x",
        purpose="p",
        languages="python",
        has_api=False,
        has_ui=True,
        has_db=False,
        risk="side-project",
    )
    assert "ui" in answers.modules()
    assert answers.lang_typescript
    assert not answers.has_lib
