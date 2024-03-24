import subprocess
import sys
from pathlib import Path

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.file import tutorial005 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_main(tmpdir):
    config_file = Path(tmpdir) / "config.txt"
    if config_file.exists():  # pragma no cover
        config_file.unlink()
        config_file.write_text("")
    result = runner.invoke(app, ["--config", f"{config_file}"])
    result = runner.invoke(app, ["--config", f"{config_file}"])
    result = runner.invoke(app, ["--config", f"{config_file}"])
    text = config_file.read_text()
    config_file.unlink()
    assert result.exit_code == 0
    assert "Config line written"
    assert "This is a single line\nThis is a single line\nThis is a single line" in text


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
