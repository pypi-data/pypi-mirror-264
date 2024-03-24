import os
import re
import subprocess
import sys
from enum import Enum
from pathlib import Path
from typing import Optional, Tuple

import click

try:
    import shellingham
except ImportError:  # pragma: nocover
    shellingham = None


from typing import Optional


class Shells(str, Enum):
    bash = "bash"
    zsh = "zsh"
    fish = "fish"
    powershell = "powershell"
    pwsh = "pwsh"


COMPLETION_SCRIPT_BASH = """
%(complete_func)s() {
    local IFS=$'\n'
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \\
                   COMP_CWORD=$COMP_CWORD \\
                   %(autocomplete_var)s=complete_bash $1 ) )
    return 0
}

complete -o default -F %(complete_func)s %(prog_name)s
"""

COMPLETION_SCRIPT_ZSH = """
#compdef %(prog_name)s

%(complete_func)s() {
  eval $(env _TYPER_COMPLETE_ARGS="${words[1,$CURRENT]}" %(autocomplete_var)s=complete_zsh %(prog_name)s)
}

compdef %(complete_func)s %(prog_name)s
"""

COMPLETION_SCRIPT_FISH = 'complete --command %(prog_name)s --no-files --arguments "(env %(autocomplete_var)s=complete_fish _TYPER_COMPLETE_FISH_ACTION=get-args _TYPER_COMPLETE_ARGS=(commandline -cp) %(prog_name)s)" --condition "env %(autocomplete_var)s=complete_fish _TYPER_COMPLETE_FISH_ACTION=is-args _TYPER_COMPLETE_ARGS=(commandline -cp) %(prog_name)s"'

COMPLETION_SCRIPT_POWER_SHELL = """
Import-Module PSReadLine
Set-PSReadLineKeyHandler -Chord Tab -Function MenuComplete
$scriptblock = {
    param($wordToComplete, $commandAst, $cursorPosition)
    $Env:%(autocomplete_var)s = "complete_powershell"
    $Env:_TYPER_COMPLETE_ARGS = $commandAst.ToString()
    $Env:_TYPER_COMPLETE_WORD_TO_COMPLETE = $wordToComplete
    %(prog_name)s | ForEach-Object {
        $commandArray = $_ -Split ":::"
        $command = $commandArray[0]
        $helpString = $commandArray[1]
        [System.Management.Automation.CompletionResult]::new(
            $command, $command, 'ParameterValue', $helpString)
    }
    $Env:%(autocomplete_var)s = ""
    $Env:_TYPER_COMPLETE_ARGS = ""
    $Env:_TYPER_COMPLETE_WORD_TO_COMPLETE = ""
}
Register-ArgumentCompleter -Native -CommandName %(prog_name)s -ScriptBlock $scriptblock
"""

_completion_scripts = {
    "bash": COMPLETION_SCRIPT_BASH,
    "zsh": COMPLETION_SCRIPT_ZSH,
    "fish": COMPLETION_SCRIPT_FISH,
    "powershell": COMPLETION_SCRIPT_POWER_SHELL,
    "pwsh": COMPLETION_SCRIPT_POWER_SHELL,
}

# TODO: Probably refactor this, copied from Click 7.x
_invalid_ident_char_re = re.compile(r"[^a-zA-Z0-9_]")


def get_completion_script(*, prog_name: str, complete_var: str, shell: str) -> str:
    cf_name = _invalid_ident_char_re.sub("", prog_name.replace("-", "_"))
    script = _completion_scripts.get(shell)
    if script is None:
        click.echo(f"Shell {shell} not supported.", err=True)
        sys.exit(1)
    return (
        script
        % dict(
            complete_func="_{}_completion".format(cf_name),
            prog_name=prog_name,
            autocomplete_var=complete_var,
        )
    ).strip()


def install_bash(*, prog_name: str, complete_var: str, shell: str) -> Path:
    # Ref: https://github.com/scop/bash-completion#faq
    # It seems bash-completion is the official completion system for bash:
    # Ref: https://www.gnu.org/software/bash/manual/html_node/A-Programmable-Completion-Example.html
    # But installing in the locations from the docs doesn't seem to have effect
    completion_path = Path.home() / f".bash_completions/{prog_name}.sh"
    rc_path = Path.home() / ".bashrc"
    rc_path.parent.mkdir(parents=True, exist_ok=True)
    rc_content = ""
    if rc_path.is_file():
        rc_content = rc_path.read_text()
    completion_init_lines = [f"source {completion_path}"]
    for line in completion_init_lines:
        if line not in rc_content:  # pragma: nocover
            rc_content += f"\n{line}"
    rc_content += "\n"
    rc_path.write_text(rc_content)
    # Install completion
    completion_path.parent.mkdir(parents=True, exist_ok=True)
    script_content = get_completion_script(
        prog_name=prog_name, complete_var=complete_var, shell=shell
    )
    completion_path.write_text(script_content)
    return completion_path


def install_zsh(*, prog_name: str, complete_var: str, shell: str) -> Path:
    # Setup Zsh and load ~/.zfunc
    zshrc_path = Path.home() / ".zshrc"
    zshrc_path.parent.mkdir(parents=True, exist_ok=True)
    zshrc_content = ""
    if zshrc_path.is_file():
        zshrc_content = zshrc_path.read_text()
    completion_init_lines = [
        "autoload -Uz compinit",
        "compinit",
        "zstyle ':completion:*' menu select",
        "fpath+=~/.zfunc",
    ]
    for line in completion_init_lines:
        if line not in zshrc_content:  # pragma: nocover
            zshrc_content += f"\n{line}"
    zshrc_content += "\n"
    zshrc_path.write_text(zshrc_content)
    # Install completion under ~/.zfunc/
    path_obj = Path.home() / f".zfunc/_{prog_name}"
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    script_content = get_completion_script(
        prog_name=prog_name, complete_var=complete_var, shell=shell
    )
    path_obj.write_text(script_content)
    return path_obj


def install_fish(*, prog_name: str, complete_var: str, shell: str) -> Path:
    path_obj = Path.home() / f".config/fish/completions/{prog_name}.fish"
    parent_dir: Path = path_obj.parent
    parent_dir.mkdir(parents=True, exist_ok=True)
    script_content = get_completion_script(
        prog_name=prog_name, complete_var=complete_var, shell=shell
    )
    path_obj.write_text(f"{script_content}\n")
    return path_obj


def install_powershell(*, prog_name: str, complete_var: str, shell: str) -> Path:
    subprocess.run(
        [
            shell,
            "-Command",
            "Set-ExecutionPolicy",
            "Unrestricted",
            "-Scope",
            "CurrentUser",
        ]
    )
    result = subprocess.run(
        [shell, "-NoProfile", "-Command", "echo", "$profile"],
        check=True,
        stdout=subprocess.PIPE,
    )
    if result.returncode != 0:  # pragma: nocover
        click.echo("Couldn't get PowerShell user profile", err=True)
        raise click.exceptions.Exit(result.returncode)
    path_str = ""
    if isinstance(result.stdout, str):  # pragma: nocover
        path_str = result.stdout
    if isinstance(result.stdout, bytes):
        try:
            # PowerShell would be predominant in Windows
            path_str = result.stdout.decode("windows-1252")
        except UnicodeDecodeError:  # pragma: nocover
            try:
                path_str = result.stdout.decode("utf8")
            except UnicodeDecodeError:
                click.echo("Couldn't decode the path automatically", err=True)
                raise click.exceptions.Exit(1)
    path_obj = Path(path_str.strip())
    parent_dir: Path = path_obj.parent
    parent_dir.mkdir(parents=True, exist_ok=True)
    script_content = get_completion_script(
        prog_name=prog_name, complete_var=complete_var, shell=shell
    )
    with path_obj.open(mode="a") as f:
        f.write(f"{script_content}\n")
    return path_obj


def install(
    shell: Optional[str] = None,
    prog_name: Optional[str] = None,
    complete_var: Optional[str] = None,
) -> Tuple[str, Path]:
    prog_name = prog_name or click.get_current_context().find_root().info_name
    assert prog_name
    if complete_var is None:
        complete_var = "_{}_COMPLETE".format(prog_name.replace("-", "_").upper())
    test_disable_detection = os.getenv("_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION")
    if shell is None and shellingham is not None and not test_disable_detection:
        shell, _ = shellingham.detect_shell()
    if shell == "bash":
        installed_path = install_bash(
            prog_name=prog_name, complete_var=complete_var, shell=shell
        )
        return shell, installed_path
    elif shell == "zsh":
        installed_path = install_zsh(
            prog_name=prog_name, complete_var=complete_var, shell=shell
        )
        return shell, installed_path
    elif shell == "fish":
        installed_path = install_fish(
            prog_name=prog_name, complete_var=complete_var, shell=shell
        )
        return shell, installed_path
    elif shell in {"powershell", "pwsh"}:
        installed_path = install_powershell(
            prog_name=prog_name, complete_var=complete_var, shell=shell
        )
        return shell, installed_path
    else:
        click.echo(f"Shell {shell} is not supported.")
        raise click.exceptions.Exit(1)
