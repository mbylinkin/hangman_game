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

Flow: `run.py` → `GameApplication` (`app/main.py`) → `ConsoleGameController` (`app/controller.py`) → `Game` (`app/model.py`) and `ConsoleView` (`app/view.py`).

- All user input/output goes through `BaseView` (`render`, `ask_new_game`, `ask_letter`, `show_message`); `ConsoleView` is the only place with `input()`/`print()`. Keep it that way — controller, model and `main.py` must stay console-free.
- `GameApplication.loop()` repeats `play_game()` while `controller.ask_new_game()`; `play_game()` drives each turn: `start_next_turn()` → `render()` → `input_letter()` → `play_turn()`, until `game_pending()` is false. The controller is injected via `GameApplication(vocabulary, controller=...)`, defaulting to `get_game_controller()`.
- `BaseGameController(view)` holds the `Game` and the view and works with any `BaseView`. `input_letter()` asks the view up to `MAX_LETTER_INPUT_TRIES` times, shows validation messages via `view.show_message`, then returns the sentinel `"*"` (counted as a wrong guess). `ConsoleGameController` only binds `ConsoleView`.
- `Game` is the single source of game state: `errors`, `guessed` letters, `turn_number` (0 = no turn started) and `guess_letter` ("" until the current turn is played). `current_word` is derived from `secret_word` + `guessed` — don't store it. `start_next_turn()` → `play_turn(letter)` per turn; `play_turn` before any turn raises `RuntimeError`. `history` is a list of frozen `Move(number, letter, hit)`, not read by the game itself.
- `GameState` (`app/const.py`): `LOST` = `MAX_GUESS_ERRORS` reached, `WON` = player guessed the word. Hidden letters are `_` in `current_word`.
- `ConsoleView` renders Jinja2 string templates from `app/templates.py`; the hangman drawing is looked up by error count in `head_ascii`/`body_ascii`/`legs_ascii` (keys 0..6, tied to `MAX_GUESS_ERRORS`).
- `WordVocabulary` (`app/input.py`) loads `data/words.txt` (one word per line, path in `app/const.py:WORDS_PATH`, resolved from the package location) and returns random words without repeats, tracking used indices.

## Tests

`tests/` mirrors the modules (`controller/`, `input/`, `main/`, `model/`, `view/`). `tests/main/test_console_transcript.py` plays two seeded games through `run.main()` and compares the whole console output with `tests/data/console_transcript.txt` byte for byte — update that file only for intended output changes (it is excluded from whitespace hooks). Controller/application tests use `FakeView` from `tests/conftest.py` (`fake_view` fixture: preset `new_game_answers`/`letters`, recorded `messages`/`rendered_states`); only `ConsoleView` tests and the console end-to-end tests in `tests/main` patch `builtins.input`. File reading is mocked via `mocker.patch('app.input.read_words_from_file', ...)` (pytest-mock). The `name-tests-test` pre-commit hook requires every file in `tests/` except `conftest.py`/`__init__.py` to be named `test_*.py` — shared test helpers go into `conftest.py`.
