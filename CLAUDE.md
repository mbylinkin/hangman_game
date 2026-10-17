# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Console Hangman game in Python, written as an MVC exercise (architecture + testing practice). Dependencies are declared in `pyproject.toml`: Jinja2 is the only runtime dependency, dev tooling is in the `dev` extra.

## Commands

```shell
pip install -e ".[dev]"
python run.py                      # play

make test                          # pytest .
make test-cov                      # HTML coverage -> tests/coverage/, fails under 80% (.coveragerc)
pytest tests/model/test_game_play.py::test_game_play_turn_guessed_letter   # single test

make lint                          # pre-commit run --all-files: ruff check --fix, ruff format, mypy (config in ruff.toml)
```

CI (`.github/workflows/ci.yml`) runs the same pre-commit hooks and `pytest --cov=app` on Python 3.10, 3.12 and 3.13 for every PR and push to `main`.

## Architecture

Flow: `run.py` → `GameApplication` (`app/main.py`) → `ConsoleGameController` (`app/controller.py`) → `Game`/`GameTurn` (`app/model.py`) and `ConsoleView` (`app/view.py`).

- `GameApplication.loop()` asks "Start new game?" and `play_game()` drives each turn: `start_next_turn()` → `render()` → `input_letter()` → `play_turn()`, until `game_pending()` is false. `get_game_controller()` is the seam for swapping in a different (e.g. GUI) controller.
- `BaseGameController` holds the `Game` and a `BaseView`; subclasses implement `input_letter()` (console version allows `MAX_LETTER_INPUT_TRIES` invalid attempts, then returns the sentinel `"*"`).
- Model state is split: `Game` keeps `current_word` / `errors`, and each `GameTurn` gets a deep copy of them, mutates its own copy in `play()`, and `Game.play_turn()` copies the result back. `GameTurn.new_turn()` builds the next turn from the previous one; `Game.state()` is computed from `current_turn`, while `validate_letter()` reads `Game.errors` / `Game.current_word` — keep both in sync when changing the model.
- `GameState` (`app/const.py`): `LOST` = `MAX_GUESS_ERRORS` reached, `WON` = player guessed the word. Hidden letters are `_` in `current_word`.
- `ConsoleView` renders Jinja2 string templates from `app/templates.py`; the hangman drawing is looked up by error count in `head_ascii`/`body_ascii`/`legs_ascii` (keys 0..6, tied to `MAX_GUESS_ERRORS`).
- `WordVocabulary` (`app/input.py`) loads `data/words.txt` (one word per line, path in `app/const.py:WORDS_PATH`, resolved from the package location) and returns random words without repeats, tracking used indices.

## Tests

`tests/` mirrors the modules (`controller/`, `input/`, `main/`, `model/`). Console input is faked with `mock.patch("builtins.input", side_effect=[...])`; file reading is mocked via `mocker.patch('app.input.read_words_from_file', ...)` (pytest-mock). The `name-tests-test` pre-commit hook requires test files to be named `test_*.py`.
