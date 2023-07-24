import contextlib
import os
import subprocess
import sys
from difflib import unified_diff
from functools import wraps
from io import StringIO
from pathlib import Path
from typing import List, Optional, Tuple

import colorama
import pygments
import typer
from black import Changed, Report
from colorama import Fore
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.python import Python3Lexer
from typer import Argument

PROJECT_DIR = Path(__file__).parent.parent

colorama.init()

lexer = Python3Lexer()
formatter = TerminalFormatter()

actions = set()


def echo(*args):
    print(*args, flush=True)


def action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        previous_dir = os.curdir
        os.chdir(PROJECT_DIR)  # make script workdir agnostic
        try:
            exit_code = func(*args, **kwargs)
        except SystemExit as e:
            return e.code
        finally:
            os.chdir(previous_dir)

        if exit_code is not None:
            return exit_code

        return 0

    actions.add(wrapper)
    return wrapper


def paint(text, color):
    return color + text + Fore.RESET


def highlight_code(code):
    return pygments.highlight(code, lexer=lexer, formatter=formatter)


def color_diff(diff):
    for line in diff:
        if line.startswith("+"):
            yield paint(line, Fore.GREEN)
        elif line.startswith("-"):
            yield paint(line, Fore.RED)
        elif line.startswith("^"):
            yield paint(line, Fore.BLUE)
        elif line.startswith("@@"):
            try:
                prefix, deleted, added, suffix = line.split()
            except ValueError:
                yield highlight_code(line)
            else:
                yield f"{prefix} {paint(deleted, Fore.RED)} {paint(added, Fore.GREEN)} {suffix}\n"
        else:
            yield highlight_code(line)


def get_diff(original_source, new_source, file):
    return color_diff(
        unified_diff(
            StringIO(original_source).readlines(),
            StringIO(new_source).readlines(),
            fromfile=str(file),
            tofile=str(file),
            n=0,
        )
    )


def get_changed_files():
    files = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True,
        check=True,
    ).stdout.decode()
    return [Path(file) for file in files.split("\n") if file.endswith(".py")]


@action
def run_flakehell(files):
    import flakehell

    flakehell.flake8_entrypoint(list(map(str, files)))


@action
def run_isort(files):
    """
    Isort doesn't provide an option to exit-zero, treat presence of any output an error
    """
    from isort.main import main as isort_main

    stdout, stderr = StringIO(), StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        isort_main([*map(str, files), f"--settings-path={PROJECT_DIR}"])

    exit_code = 0
    stderr_result, stdout_result = stderr.getvalue(), stdout.getvalue()
    if stderr_result:
        exit_code = 1
        print(stderr_result, file=sys.stderr)
    if stdout_result:
        exit_code = 1
        print(stdout_result)

    return exit_code


@action
def run_black(files):
    """
    Run black, but let it output to console only if it changed any files
    """
    import black
    import click

    original_done = Report.done
    original_echo = click.echo
    original_out = black.out

    black.out = click.echo = lambda *args, **kwargs: None

    exit_code = 0

    def done_patch(self, src, changed):
        nonlocal exit_code
        if changed is Changed.YES:  # ok, black changed a file, let it complain about that
            click.echo = original_echo
            black.out = original_out
            exit_code = 1
        original_done(self, src, changed)

    Report.done = done_patch

    try:
        black.main.main(map(str, files))
    except SystemExit as e:
        return max(exit_code, e.code)
    finally:
        Report.done = original_done
        click.echo = original_echo
        black.out = original_out


@action
def run_autoflake(files: List[Path]):
    """
    Run autoflake and display removed imports
    """
    import autoflake

    exit_code = 0
    for file in files:
        original_source = file.read_text()
        new_source = autoflake.fix_code(original_source, remove_all_unused_imports=True, expand_star_imports=True)
        if new_source != original_source:
            echo(f"Removed unused import(s):\n{''.join(get_diff(original_source, new_source, file))}")
            file.write_text(new_source)
            exit_code = 1
    return exit_code


@action
def run_flynt(files: List[Path]):
    """
    Run flynt and display changed strings
    """
    import flynt
    from flynt import state
    from flynt.api import fstringify_files

    # flynt uses global state
    state.aggressive = True
    state.quiet = True

    # using this public methods to trace changes
    orig_fstringify = flynt.api.fstringify_code_by_line
    orig_fstringify_concats = flynt.api.fstringify_concats

    current_file: Optional[Path] = None
    current_original_source: Optional[str] = None

    def traceable_file_generator():
        nonlocal current_file
        for file in files:
            current_file = file
            yield file

    def fstringify(code, *args, **kwargs):
        # Known to be called first, so take original code from here
        nonlocal current_original_source
        current_original_source = code

        return orig_fstringify(code, *args, **kwargs)

    def fstringify_concats(code, *args, **kwargs):
        # if any of this errors raised, I fucked up somehow or library was updated
        if current_original_source is None or current_file is None:
            raise RuntimeError("Unable to trace file changed by fstringify")
        if current_file.read_text() != current_original_source:
            raise RuntimeError("Traced original code differs from traced original file")

        new_source, *other = orig_fstringify_concats(code, *args, **kwargs)
        if new_source != current_original_source:
            echo(
                f"Changing this file to use f-strings:\n"
                f"{''.join(get_diff(current_original_source, new_source, current_file))}",
            )

        return (new_source, *other)

    flynt.api.fstringify_code_by_line = fstringify
    flynt.api.fstringify_concats = fstringify_concats

    try:
        return fstringify_files(
            traceable_file_generator(),
            multiline=True,
            len_limit=120,  # bad, bad, bad. We should read line_length from pyproject.toml, but I'm lazy
            transform_concat=True,
        )
    finally:
        flynt.api.fstringify_code_by_line = orig_fstringify
        flynt.api.fstringify_concats = orig_fstringify_concats


ACTIONS_TO_RUN = [
    run_flynt,
    run_autoflake,
    run_isort,
    run_black,
    run_flakehell,
]

assert (
    set(ACTIONS_TO_RUN) == actions
), f"Some actions were registered, but not added to ACTIONS_TO_RUN: {actions - set(ACTIONS_TO_RUN)}"


def execute_actions(files: List[Path]) -> Tuple[List[Tuple[str, int]], int]:
    exit_code = 0
    executed_actions: List[Tuple[str, int]] = []
    if not files:
        raise ValueError("Files to check are required")

    for action_to_run in ACTIONS_TO_RUN:
        action_name = action_to_run.__name__[4:]
        echo(f"Running {action_name}")
        sys.stderr.flush()
        sys.stdout.flush()
        action_exit_code = action_to_run(files)
        executed_actions.append((action_name, action_exit_code))
        if action_exit_code:
            exit_code = 1
            echo(f"Finished with exit code {exit_code}\n")
        else:
            echo()

    return executed_actions, exit_code


def main(files: Optional[List[Path]] = Argument(None, file_okay=True)):  # noqa: B008 (function call in default arg)
    if not files:
        files = get_changed_files()

    if not files:
        echo("No Python files provided, nothing to do 😴")
        sys.exit(0)

    _, exit_code = execute_actions(files)

    raise typer.Exit(exit_code)


if __name__ == "__main__":
    typer.run(main)
