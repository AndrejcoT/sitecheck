# Devlog — 2026-03-20

## Session goal

Set up the repository structure and begin turning the project into a real Python CLI.

## What I worked on

- Created the GitHub repository
- Created the main folder structure
- Added the `src/sitecheck/` package directory
- Added the `tests`, `docs`, `examples`, and `.github` folders
- Started working on the first CLI file
- Began learning how command-line arguments work in Python

## What went well

- The repo structure is now in place
- I understand the difference between the repo root and the Python package folder
- I have a starting CLI flow using `sys.argv`
- The project now feels real instead of just being an idea

## What confused me

- I was not sure at first how to check what was written in the terminal with python.
- I was struggling with formating and writing the code in `cli.py`. The first iteration was really bad.
- I struggled with setting up different functions for each of the commands. The first itteration was one big function.
- I also needed to understand what `.github`, `CHANGELOG.md`, and `CONTRIBUTING.md` are for


## What I learned

- The root project folder and the Python package folder are not the same thing
- `__init__.py` helps define a Python package
- `cli.py` is where the command-line entry point starts
- `sys.argv` is a basic way to read command-line arguments
- A cleaner CLI structure should use functions like:
  - `show_help()`
  - `scan(path)`
  - `main()`

## Current state of the project

Right now the project has:
- a GitHub repo
- a clean folder structure
- a first CLI attempt
- a direction for becoming a real installable Python CLI

## Next steps

- improve the structure of `cli.py`
- make the help output more useful
- add a proper `main()` function
- create and test `pyproject.toml`
- create and activate the virtual environment
- install the project in editable mode
- make `sitecheck --help` work as a real command

## Problems to solve soon

- make sure the package installs correctly
- understand how `pyproject.toml` connects the command name to `main()`
- move from a basic script feeling to a proper Python project structure

## One sentence summary

Today I turned the project from an idea into a real repo with structure and the beginning of a working CLI.