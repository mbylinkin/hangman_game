# Hangman game

## About

[Hangman game](https://en.wikipedia.org/wiki/Hangman_(game)) is a simple text-based game that allows you to play against the computer. The computer selects a word and you try to guess it by suggesting letters. With each guess, the computer tells you if the letter is in the word or not. If you guess all the letters of the word correctly, you win. If you make too many mistakes, you lose.

## Installation

To install the application, clone the repository and install the requirements.
```shell
pip install -r requirements.txt
```

## Running game

To run game, execute run.py:

```shell
python -m run.py
```

## Gameplay

1. After starting game answer "y" on question "Start new game? (y/n)"
2. Input letters to guess the word
3. After game end see the result (win/loose)
4. If you want to play another game, "y" on question "Start new game? (y/n)", "n" - if not

## Application design

Application is written in [MVC style](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller), the purpose was to get some practice in
* architectute design of application
* writing tests


<details>
<summary>Directory structure</summary>

```shell
├── app
│   ├── const.py
│   ├── controller.py
│   ├── input.py
│   ├── main.py
│   ├── model.py
│   ├── templates.py
│   └── view.py
├── data
│   └── words.txt
├── tests
│   └── ...
├── LICENSE
├── Makefile
├── README.md
├── requirements.txt
├── ruff.toml
└── run.py
```

</details>

* [run.py](run.py) File for creating and running application
* [app/main.py](app/main.py) Holds class GameApplication which holds Controller class and initiates main game loop
* [app/controller.py](app/controller.py) Holds controller class, which holds Model (Game) class, View class and is responsible for communication with model and rendering game
* [app/model.py](app/model.py) Holds Logic of the Game
* [app/view.py](app/view.py) A view for rendering game
* [app/template.py](app/template.py) A templates file for rendering
* [app/input.py](app/input.py) Vocabulary class for generating random word
* [data/words.txt](data/words.txt) Vocabulary for generating random words. Used in WordVocabulary class
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

## Further development

Application is written for console mode, but due to MVC pattern game logic, client view is separated from each other.

So, It is possible to write classes:
* GUIGameController
* GUIViev

and implement GameApplication class with new controller (GUIGameController)

An example of GUI can be taken [from here](https://realpython.com/hangman-python-pysimplegui/).

Or maybe somewhere else.
