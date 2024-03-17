from __future__ import annotations

from app.const import GameState
from app.const import MAX_LETTER_INPUT_TRIES
from app.model import Game
from app.view import BaseView
from app.view import ConsoleView


class BaseGameController:
    def __init__(self) -> None:
        self.current_game: Game = None  # type: ignore
        self.view: BaseView = None  # type: ignore
        self.max_input_tries = MAX_LETTER_INPUT_TRIES

    def start_game(self, random_word: str) -> None:
        self.current_game = Game(random_word)

    def start_next_turn(self) -> None:
        self.current_game.start_next_turn()

    def play_turn(self, guess_letter: str) -> GameState:
        return self.current_game.play_turn(guess_letter)

    def input_letter(self) -> str:
        raise NotImplementedError()

    def validate_letter(self, guess_letter: str) -> tuple[bool, str]:
        if len(guess_letter) != 1:
            return False, 'Your input is not a single letter. Try again.'
        elif not guess_letter.isalpha():
            return False, 'Your input is not a letter. Try again.'
        elif guess_letter in self.current_game.errors or guess_letter in self.current_game.current_word:
            return False, 'You already guessed this letter. Try again.'
        return True, guess_letter

    def render(self) -> None:
        self.view.render(self.current_game)

    def game_state(self) -> GameState:
        return self.current_game.state()

    def game_pending(self) -> bool:
        return self.game_state() == GameState.ONGOING


class ConsoleGameController(BaseGameController):
    def __init__(self) -> None:
        super().__init__()
        self.view = ConsoleView()

    def input_letter(self) -> str:
        input_try = 0
        while True:
            input_try = input_try + 1
            guess_letter = input("Input letter:").lower()
            success_try, validate_message = self.validate_letter(guess_letter)

            if success_try:
                return guess_letter
            else:
                print(validate_message)

            if not success_try and input_try >= self.max_input_tries:
                print("Number of tries exceeded.")
                break

        return "*"
