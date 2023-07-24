## Configure the template
  - `brew install gettext` (Make sure this requirement is installed to suppress the `envsubst: command not found` error)
  - Run `./setup.sh` and follow the steps as shown in the prompts.

## Requirements
* Brew
  * For installation see: https://docs.brew.sh/Installation
* Python
  *  v3.10.0 (exact version) using [Pyenv](https://github.com/pyenv/pyenv)
      * `brew install pyenv`
      * `pyenv install 3.10.0`
      * `pyenv versions` to confirm that **3.10.0** is in the list of Python versions
  * Inside the project directory
      * `rm -rf .venv` to remove old environment
      * `pyenv local 3.10.0` to set specific Python version at project level (not OS level)
      * `python --version` to check if it's **3.10.0**. If not, then
          * `echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc` or `~/.bash_profile`
          * `echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc` or `~/.bash_profile`
          * `echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.zshrc` or `~/.bash_profile`
      * Re-open shell and `python --version` to check if it's **3.10.0** at project level
* Poetry
  * `pip install poetry`
  * Inside the project directory
      * `poetry shell` to activate poetry virtual environment
      * `python --version` to confirm that **3.10.0** inside the environment as well
* Setup script
  * `brew install gettext`

## Setup the development environment
* Confirm you have all system requirements above
* Clone the repository to your local machine
* Download & install dependencies by running `poetry install`


## Working with requirements/dependencies
 - For adding a requirement, you can run: `poetry add {requirement}`
 - For adding a dev requirement, you can run: `poetry add {requirement} --dev`
 - For updating a requirement, you can run: `poetry update {requirement}`
 - For removal of a requirement, you can run: `poetry remove {requirement}`

-------------------------------------------------
## Run the server
- `uvicorn friendlyeats.app:app --host 0.0.0.0 --port 80 --reload`

## Run lint & format
- `isort .` - sort package imports
- `black .` - format the code


---------------------------------------------
## Run pre-commit hook (optional)
- `poetry shell` - start from the Poetry env
- `python tools/setup_pre_commit.py` - install pre-commit hook (if no errors --> pre-commit is ON)
- `python tools/pre_commit.py` - run pre-commit manually against file you've made changes to

