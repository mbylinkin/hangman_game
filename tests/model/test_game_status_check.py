from __future__ import annotations

from app.model import game_state_check
from app.model import GameState
from app.model import GameTurn


def test_lost() -> None:
    """
    Test for the scenario where the player loses. It initializes a GameTurn object with specific attributes
    and then asserts that the game state check function returns the expected GameState for the given scenario.
    """
    game_turn = GameTurn(
        turn_number=6,
        secret_word="hello",
        current_word="_____",
        errors=["a", "b", "c", "d", "e", "f"],
    )
    assert game_state_check(game_turn) == GameState.LOST


def test_won() -> None:
    """
    Test function to check if the player wins the game.
    """
    game_turn = GameTurn(
        turn_number=6,
        secret_word="hello",
        current_word="hello",
        errors=["a", "b", "c", "d", "e"],
    )
    assert game_state_check(game_turn) == GameState.WON


def test_ongoing() -> None:
    """
    Function to test the ongoing game state by creating a game turn and checking the game state.
    """
    game_turn = GameTurn(
        turn_number=6,
        secret_word="hello",
        current_word="hel_o",
        errors=["a", "b", "c", "d", "e"],
    )
    assert game_state_check(game_turn) == GameState.ONGOING
