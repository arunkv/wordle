# AGENTS.md

## Purpose
- This repository contains a Python Wordle solver with multiple solving strategies in `/home/runner/work/wordle/wordle/src`.

## Environment
- Use Python 3.12.
- Install dependencies from repository root:
  - `python -m pip install --upgrade pip`
  - `pip install -r requirements.txt`

## Common Commands
- Run solver:
  - `python /home/runner/work/wordle/wordle/src/wordle.py -d /home/runner/work/wordle/wordle/words/wordle-nyt-words-14855.txt`
- Run unit tests:
  - `PYTHONPATH=/home/runner/work/wordle/wordle/src python -m unittest /home/runner/work/wordle/wordle/src/solvertests.py`
- Run lint (matches CI):
  - `pylint --ignore=solvertests.py $(git ls-files '*.py')`

## Change Guidelines
- Keep changes minimal and scoped to the requested task.
- Do not commit generated binaries or temporary files.
- Preserve existing CLI behavior in `src/wordle.py` unless explicitly requested.
- Add or update tests in `src/solvertests.py` when changing solver logic.

## Repository Notes
- Word list files are under `/home/runner/work/wordle/wordle/words`.
- CI includes Pylint, CodeQL, and Qodana workflows.
