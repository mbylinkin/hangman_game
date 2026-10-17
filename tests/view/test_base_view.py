from __future__ import annotations

import pytest

from app.model import Game
from app.view import BaseView


def test_base_view_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError, match='abstract'):
        BaseView()  # type: ignore[abstract]


def test_incomplete_view_cannot_be_instantiated() -> None:
    """
    A view that misses a method fails on creation, not in the middle of a game.
    """

    class NoInputView(BaseView):
        def render(self, current_game: Game) -> None:
            pass

        def show_message(self, message: str) -> None:
            pass

    with pytest.raises(TypeError, match='ask_letter.*ask_new_game|ask_new_game.*ask_letter'):
        NoInputView()  # type: ignore[abstract]
