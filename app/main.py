from __future__ import annotations

from app.controller import BaseGameController
from app.controller import ConsoleGameController
from app.input import WordVocabulary


def get_game_controller() -> BaseGameController:
    return ConsoleGameController()


class GameApplication:
    """Game application."""

    def __init__(self, vocabulary: WordVocabulary, controller: BaseGameController | None = None) -> None:
        self.controller = controller or get_game_controller()
        self.vocabulary = vocabulary

    def loop(self) -> None:
        while self.controller.ask_new_game():
            self.play_game()

    def play_game(self) -> None:
        self.controller.start_game(self.vocabulary.random_word())
        while self.controller.game_pending():
            self.controller.start_next_turn()
            self.controller.render()
            guess_letter = self.controller.input_letter()
            self.controller.play_turn(guess_letter)
        self.controller.render()
