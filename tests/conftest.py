from __future__ import annotations

import pytest

from hangman.const import GameState
from hangman.model import Game
from hangman.view import BaseView


class FakeView(BaseView):
    """
    View for tests: answers come from preset lists, output is recorded instead of printed.
    """

    def __init__(self) -> None:
        self.new_game_answers: list[bool] = []
        self.letters: list[str] = []
        self.messages: list[str] = []
        self.rendered_states: list[GameState] = []

    def ask_new_game(self) -> bool:
        return self.new_game_answers.pop(0)

    def ask_letter(self) -> str:
        return self.letters.pop(0)

    def show_message(self, message: str) -> None:
        self.messages.append(message)

    def render(self, current_game: Game) -> None:
        self.rendered_states.append(current_game.state())


@pytest.fixture
def fake_view() -> FakeView:
    return FakeView()
