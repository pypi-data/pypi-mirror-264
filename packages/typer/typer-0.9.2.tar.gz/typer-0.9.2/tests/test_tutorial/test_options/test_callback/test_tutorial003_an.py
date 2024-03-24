import os
import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.options.callback import tutorial003_an as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_1():
    result = runner.invoke(app, ["--name", "Camila"])
    assert result.exit_code == 0
    assert "Validating name" in result.output
    assert "Hello Camila" in result.output


def test_2():
    result = runner.invoke(app, ["--name", "rick"])
    assert result.exit_code != 0
    assert "Invalid value for '--name': Only Camila is allowed" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout


def test_completion():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL003_AN.PY_COMPLETE": "complete_bash",
            "COMP_WORDS": "tutorial003_an.py --",
            "COMP_CWORD": "1",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "--name" in result.stdout
