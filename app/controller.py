from __future__ import annotations

from app.const import GameState
from app.const import MAX_LETTER_INPUT_TRIES
from app.model import Game
from app.view import BaseView
from app.view import ConsoleView


class BaseGameController:
    def __init__(self, view: BaseView) -> None:
        self.current_game: Game | None = None
        self.view = view
        self.max_input_tries = MAX_LETTER_INPUT_TRIES

    @property
    def game(self) -> Game:
        """Current game; raises if no game is started."""
        if self.current_game is None:
            raise RuntimeError('Game is not started, call start_game() first.')
        return self.current_game

    def start_game(self, random_word: str) -> None:
        self.current_game = Game(random_word)

    def start_next_turn(self) -> None:
        self.game.start_next_turn()

    def play_turn(self, guess_letter: str) -> GameState:
        return self.game.play_turn(guess_letter)

    def ask_new_game(self) -> bool:
        return self.view.ask_new_game()

    def input_letter(self) -> str:
        """
        Ask the player for a letter until it is valid, at most max_input_tries times.
        Returns "*" when the tries are exceeded; it counts as a wrong guess.
        """
        for _ in range(self.max_input_tries):
            guess_letter = self.view.ask_letter().lower()
            success_try, validate_message = self.validate_letter(guess_letter)
            if success_try:
                return guess_letter
            self.view.show_message(validate_message)

        self.view.show_message("Number of tries exceeded.")
        return "*"

    def validate_letter(self, guess_letter: str) -> tuple[bool, str]:
        if len(guess_letter) != 1:
            return False, 'Your input is not a single letter. Try again.'
        elif not guess_letter.isalpha():
            return False, 'Your input is not a letter. Try again.'
        elif guess_letter in self.game.errors or guess_letter in self.game.current_word:
            return False, 'You already guessed this letter. Try again.'
        return True, guess_letter

    def render(self) -> None:
        self.view.render(self.game)

    def game_state(self) -> GameState:
        return self.game.state()

    def game_pending(self) -> bool:
        return self.game_state() == GameState.ONGOING


class ConsoleGameController(BaseGameController):
    def __init__(self) -> None:
        super().__init__(ConsoleView())
