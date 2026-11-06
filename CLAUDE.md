# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Console Hangman game in Python, written as an MVC exercise (architecture + testing practice). Dependencies are declared in `pyproject.toml`: there are no runtime dependencies (standard library only, tkinter for the GUI), dev tooling is in the `dev` dependency group (`[dependency-groups]`), pinned in `uv.lock`.

## Commands

The dev environment is managed by uv: run every command through `uv run` (no virtualenv activation; the `make` targets already do it).

```shell
uv sync                            # create/update .venv from uv.lock (game in editable mode + dev group)
uv run hangman                     # play in the console (same as `python run.py` / `python -m hangman`)
uv run hangman --gui               # play in a tkinter window
uv add --group dev <pkg>           # add a dev tool: updates pyproject.toml and uv.lock together

make test                          # uv run pytest .
make test-cov                      # HTML coverage -> tests/coverage/, fails under 95% (.coveragerc; raise it as coverage grows, never lower it)
uv run pytest tests/model/test_game_play.py::test_game_play_turn_guessed_letter   # single test

make lint                          # pre-commit run --all-files: every hook in .pre-commit-config.yaml (list below)
make check                         # lint + test-cov: every check; it must pass before a change is done
```

`make lint` runs: ruff (lint with `--fix`, format; `ruff.toml`), mypy, import-linter (MVC layers, tkinter only in `hangman.gui`; `[tool.importlinter]` in `pyproject.toml`), ast-grep (`print`/`input` only in `hangman/view.py`; rules and their tests in `ast-grep/`, `sgconfig.yml`), deptry (undeclared/unused dependencies), betterleaks (secrets in staged changes), jactionlint (workflows, `dependabot.yml`), agnix (`CLAUDE.md`/`AGENTS.md`), typos (`_typos.toml`), rumdl (Markdown; `.rumdl.toml`). Tool versions are pinned in `.pre-commit-config.yaml` only.

CI (`.github/workflows/ci.yml`) runs `make lint`, `make test-cov` on Python 3.11, 3.12 and 3.13, and a Betterleaks scan of the whole git history, on every PR, push to `main` and weekly. CI sets `UV_LOCKED=1`: a `pyproject.toml` change without a matching `uv.lock` fails.

## Rules for changes

- `make check` must pass before a change is done; CI runs the same targets.
- Never disable a lint rule, contract or hook, or lower the coverage floor, to get a change through. An exception is narrow (one path and one rule, or one identifier), carries a reason in a comment, and needs a human decision.
- `tests/data/console_transcript.txt` is expected output: change it only for an intended console output change.
- `uv.lock` is generated: never edit it by hand; change dependencies with `uv add` / `uv remove` / `uv lock` and commit it together with `pyproject.toml`.

## Architecture

Flow: `run.py` → `GameApplication` (`hangman/main.py`) → `ConsoleGameController` (`hangman/controller.py`) → `Game` (`hangman/model.py`) and `ConsoleView` (`hangman/view.py`).

- All user input/output goes through the abstract `BaseView` (`render`, `ask_new_game`, `ask_letter`, `show_message` — all `@abstractmethod`, a view missing one cannot be instantiated); `ConsoleView` is the only place with `input()`/`print()`. Keep it that way — controller, model and `main.py` must stay console-free.
- `TkView` (`hangman/gui.py`) is the window view. Its `ask_letter()` blocks in `root.wait_variable()` (a nested Tk event loop) until a letter button/key is pressed, so the pull-style controller works unchanged. Closing the window while waiting raises `GameClosed`, caught in `run_gui()`. tkinter is imported only in `hangman/gui.py` and only for `run.py --gui` — keep the console path tkinter-free.
- `GameApplication.loop()` repeats `play_game()` while `controller.ask_new_game()`; `play_game()` drives each turn: `start_next_turn()` → `render()` → `input_letter()` → `play_turn()`, until `game_pending()` is false. The controller is injected via `GameApplication(vocabulary, controller=...)`, defaulting to `get_game_controller()`.
- `BaseGameController(view)` holds the `Game` and the view and works with any `BaseView`. `input_letter()` asks the view up to `MAX_LETTER_INPUT_TRIES` times, shows validation messages via `view.show_message`, then returns the sentinel `"*"` (counted as a wrong guess). `ConsoleGameController` only binds `ConsoleView`.
- `Game` is the single source of game state: `errors`, `guessed` letters, `turn_number` (0 = no turn started) and `guess_letter` ("" until the current turn is played). `current_word` is derived from `secret_word` + `guessed` — don't store it. `start_next_turn()` → `play_turn(letter)` per turn; `play_turn` before any turn raises `RuntimeError`. `history` is a list of frozen `Move(number, letter, hit)`, not read by the game itself.
- `GameState` (`hangman/const.py`): `LOST` = `MAX_GUESS_ERRORS` reached, `WON` = player guessed the word. Hidden letters are `_` in `current_word`.
- `ConsoleView` renders the string templates from `hangman/templates.py` with `str.format` (`{name}` placeholders, literal braces must be doubled; a misspelled placeholder raises `KeyError`); the hangman drawing is looked up by error count in `head_ascii`/`body_ascii`/`legs_ascii` (keys 0..6, tied to `MAX_GUESS_ERRORS`).
- Entry point is `hangman/cli.py:main(argv)` (`[project.scripts] hangman`); `run.py` and `hangman/__main__.py` only call it.
- `WordVocabulary` (`hangman/input.py`) loads `hangman/data/words.txt` — package data (`[tool.setuptools.package-data]`), so it ships with `pip install .`; path in `hangman/const.py:WORDS_PATH` and returns random words without repeats, tracking used indices.

## Tests

`tests/` mirrors the modules (`cli/`, `controller/`, `gui/`, `input/`, `main/`, `model/`, `view/`). GUI tests share one hidden session `Tk` root and get a `Toplevel` per test (`tk_view` fixture; a `Tk()` per test intermittently fails on Windows); `autoplay()` in `tests/gui/conftest.py` presses letters on Tk timers while `ask_letter()` waits. Without a display they are skipped; CI runs them under `xvfb-run` with `HANGMAN_REQUIRE_GUI=1`, which turns that skip into a failure. `tests/main/test_console_transcript.py` plays two seeded games through `hangman.cli.main([])` and compares the whole console output with `tests/data/console_transcript.txt` byte for byte — update that file only for intended output changes (it is excluded from whitespace hooks). Controller/application tests use `FakeView` from `tests/conftest.py` (`fake_view` fixture: preset `new_game_answers`/`letters`, recorded `messages`/`rendered_states`); only `ConsoleView` tests and the console end-to-end tests in `tests/main` patch `builtins.input`. File reading is mocked via `mocker.patch('hangman.input.read_words_from_file', ...)` (pytest-mock). The `name-tests-test` pre-commit hook requires every file in `tests/` except `conftest.py`/`__init__.py` to be named `test_*.py` — shared test helpers go into `conftest.py`.
