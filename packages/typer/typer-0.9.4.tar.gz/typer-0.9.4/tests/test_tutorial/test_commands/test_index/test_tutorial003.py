import subprocess
import sys

from typer.testing import CliRunner

from docs_src.commands.index import tutorial003 as mod

app = mod.app

runner = CliRunner()


def test_no_arg():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "[OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Commands" in result.output
    assert "create" in result.output
    assert "delete" in result.output


def test_create():
    result = runner.invoke(app, ["create"])
    assert result.exit_code == 0
    assert "Creating user: Hiro Hamada" in result.output


def test_delete():
    result = runner.invoke(app, ["delete"])
    assert result.exit_code == 0
    assert "Deleting user: Hiro Hamada" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
