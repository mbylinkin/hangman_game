from __future__ import annotations

from app.model import game_state_check
from app.model import GameState


def test_lost() -> None:
    """
    The player loses when the number of errors reaches MAX_GUESS_ERRORS.
    """
    assert game_state_check("_____", ["a", "b", "c", "d", "e", "f"]) == GameState.LOST


def test_won() -> None:
    """
    The player wins when no hidden letters are left.
    """
    assert game_state_check("hello", ["a", "b", "c", "d", "e"]) == GameState.WON


def test_ongoing() -> None:
    """
    The game goes on while there are hidden letters and errors are below the limit.
    """
    assert game_state_check("hel_o", ["a", "b", "c", "d", "e"]) == GameState.ONGOING
