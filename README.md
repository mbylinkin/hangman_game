# Hangman game

## About

[Hangman game](https://en.wikipedia.org/wiki/Hangman_(game)) is a simple text-based game that allows you to play against the computer. The computer selects a word and you try to guess it by suggesting letters. With each guess, the computer tells you if the letter is in the word or not. If you guess all the letters of the word correctly, you win. If you make too many mistakes, you lose.

## Installation

Python 3.10+ is required. The game has no runtime dependencies.

To play, install it from a clone (or straight from GitHub) — this adds the `hangman` command:
```shell
pip install .
pip install git+https://github.com/mbylinkin/hangman_game.git
```

For development, install it in editable mode with development dependencies:
```shell
pip install -e ".[dev]"
```

## Running game

In the console:

```shell
hangman
```

In a window (tkinter):

```shell
hangman --gui
```

Without installing, from a clone: `python run.py [--gui]` or `python -m app [--gui]`.

Click letter buttons or type letters on the keyboard; closing the window ends the game.
tkinter is part of the standard library on Windows and macOS; on Linux it may need a system package (e.g. `sudo apt install python3-tk`).
The console game works without it.

## Gameplay

1. After starting game answer "y" on question "Start new game? (y/n)"
2. Input letters to guess the word
3. After game end see the result (win/lose)
4. If you want to play another game, answer "y" on question "Start new game? (y/n)", "n" - if not

## Application design

Application is written in [MVC style](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller), the purpose was to get some practice in
* architecture design of application
* writing tests


<details>
<summary>Directory structure</summary>

```shell
├── app
│   ├── data
│   │   └── words.txt
│   ├── __main__.py
│   ├── cli.py
│   ├── const.py
│   ├── controller.py
│   ├── gui.py
│   ├── input.py
│   ├── main.py
│   ├── model.py
│   ├── templates.py
│   └── view.py
├── tests
│   └── ...
├── LICENSE
├── Makefile
├── README.md
├── pyproject.toml
├── ruff.toml
└── run.py
```

</details>

* [app/cli.py](app/cli.py) Command line entry point: the `hangman` command, `python -m app` and [run.py](run.py)
* [app/main.py](app/main.py) Holds class GameApplication which holds Controller class and initiates main game loop
* [app/controller.py](app/controller.py) Holds controller class, which holds Model (Game) class, View class and is responsible for communication with model and rendering game
* [app/model.py](app/model.py) Holds Logic of the Game
* [app/view.py](app/view.py) View interface `BaseView` and the console view
* [app/gui.py](app/gui.py) Tkinter window view `TkView`
* [app/templates.py](app/templates.py) A templates file for rendering
* [app/input.py](app/input.py) Vocabulary class for generating random word
* [app/data/words.txt](app/data/words.txt) Vocabulary for generating random words, packaged with the game. Used in WordVocabulary class
* [tests](tests) a folder, containing tests


## Testing
pytest library is used for testing.

Commands for running tests and coverage are in [Makefile](https://opensource.com/article/18/8/what-how-makefile).
For tests run
```shell
make test
```
For test coverage, run
```shell
make test-cov
```
For tests and tests coverage run
```shell
make all
```

test-coverage files are saved to tests/coverage directory

## Linting

[pre-commit](https://pre-commit.com/) runs [ruff](https://docs.astral.sh/ruff/) (lint + format, config in [ruff.toml](ruff.toml)) and mypy.
Install the git hook once after cloning:
```shell
pre-commit install
```
Run all checks manually:
```shell
make lint
```

## Further development

Due to MVC pattern game logic and user interface are separated:
all user input and output goes through the view interface `BaseView` (`render`, `ask_new_game`, `ask_letter`, `show_message`),
the controller and the game model do not use the console or the window.

There are two views: `ConsoleView` and the tkinter `TkView`. To add another user interface it is enough to write
a `BaseView` subclass and run the game with it:
```python
GameApplication(vocabulary, controller=BaseGameController(MyView()))
```

The controller asks the view for input and waits for the answer. `TkView` does it with tkinter `wait_variable()`,
which keeps processing window events until the player presses a letter.
