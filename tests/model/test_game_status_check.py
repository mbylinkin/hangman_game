from __future__ import annotations

from app.model import game_state_check
from app.model import GameState
from app.model import GameTurn


def test_player_1_wins() -> None:
    """
    Test for the scenario where player 1 wins. It initializes a GameTurn object with specific attributes
    and then asserts that the game state check function returns the expected GameState for the given scenario.
    """
    game_turn = GameTurn(
        turn_number=6,
        secret_word="hello",
        current_word="_____",
        errors=["a", "b", "c", "d", "e", "f"],
    )
    assert game_state_check(game_turn) == GameState.PLAYER_1_WINS


def test_player_2_wins() -> None:
    """
    Test function to check if player 2 wins the game.
    """
    game_turn = GameTurn(
        turn_number=6,
        secret_word="hello",
        current_word="hello",
        errors=["a", "b", "c", "d", "e"],
    )
    assert game_state_check(game_turn) == GameState.PLAYER_2_WINS


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
