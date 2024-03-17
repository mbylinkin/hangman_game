from __future__ import annotations

from app.controller import BaseGameController
from app.controller import ConsoleGameController
from app.input import WordVocabulary


def get_game_controller() -> BaseGameController:
    return ConsoleGameController()


class GameApplication:
    """Game application."""

    def __init__(self, vocabulary: WordVocabulary) -> None:
        self.controller = get_game_controller()
        self.vocabulary = vocabulary

    def loop(self) -> None:
        while True:
            answer = input('Start new game? (y/n):').lower()
            if answer != 'y':
                break

            self.play_game()

    def play_game(self) -> None:
        self.controller.start_game(self.vocabulary.random_word())
        while self.controller.game_pending():
            self.controller.start_next_turn()
            self.controller.render()
            guess_letter = self.controller.input_letter()
            self.controller.play_turn(guess_letter)
        self.controller.render()
