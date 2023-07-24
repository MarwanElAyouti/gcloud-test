import argparse
import os
import stat
import sys
from datetime import datetime
from pathlib import Path

TOOLS_DIR = Path(__file__).parent
PROJECT_DIR = TOOLS_DIR.parent
HOOK_PATH = PROJECT_DIR / ".git" / "hooks" / "pre-commit"
PYTHON_PATH = Path(sys.executable)
SCRIPT_PATH = TOOLS_DIR / "pre_commit.py"
PLACEHOLDER = f"This hook is generated with {__file__}"

HOOK_TEXT = f"""
#!/bin/sh
# {PLACEHOLDER} at {datetime.now()}

{PYTHON_PATH.absolute()} {SCRIPT_PATH.absolute()}
"""
REQUIREMENTS = ["flakehell", "autoflake", "flynt", "black", "isort"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--force", action="store_true", default=False)
    args = parser.parse_args()
    update(force=args.force)


def error(msg, code=1):
    print(f"Error: {msg}", file=sys.stderr)
    exit(code)


def update(force=False):
    if sys.exec_prefix == sys.base_exec_prefix:
        error("You must run the script with venv interpreter")

    bin_dir = Path(sys.exec_prefix) / "bin"
    for requirement in REQUIREMENTS:
        if not (bin_dir / requirement).exists():
            error(f"{requirement} not found in {bin_dir}")

    action = "configured"

    if HOOK_PATH.exists() and PLACEHOLDER not in HOOK_PATH.read_text():
        if force:
            action = "overwritten"
        else:
            error(f"Unrecognized hook at {HOOK_PATH.relative_to(PROJECT_DIR)} already exists, use -f to overwrite it")
    elif HOOK_PATH.exists():
        action = "updated"

    HOOK_PATH.write_text(HOOK_TEXT)
    os.chmod(HOOK_PATH, os.stat(HOOK_PATH).st_mode | stat.S_IEXEC)  # make file executable

    print(rf"{HOOK_PATH.relative_to(PROJECT_DIR)} is {action} \o/")


if __name__ == "__main__":
    main()
