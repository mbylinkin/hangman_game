from __future__ import annotations

import pytest

from hangman.const import GameState
from hangman.model import Game
from hangman.model import Move


@pytest.fixture
def game_fixture() -> Game:
    """
    Fixture for the game with the secret word "test".
    """
    return Game("test")


def test_game_next_turn(game_fixture: Game) -> None:
    """
    Starting a turn increments the turn number and does not change the word or errors.
    """
    game_fixture.start_next_turn()
    assert game_fixture.turn_number == 1
    assert game_fixture.guess_letter == ""
    assert game_fixture.current_word == "____"
    assert game_fixture.errors == []


def test_game_next_turn_resets_guess_letter(game_fixture: Game) -> None:
    game_fixture.start_next_turn()
    game_fixture.play_turn("t")
    game_fixture.start_next_turn()
    assert game_fixture.turn_number == 2
    assert game_fixture.guess_letter == ""
    assert game_fixture.current_word == "t__t"


def test_game_play_turn_not_guessed_letter(game_fixture: Game) -> None:
    """
    Test the game play turn with letter not guessed.
    """
    game_fixture.start_next_turn()
    assert game_fixture.play_turn("a") == GameState.ONGOING
    assert game_fixture.turn_number == 1
    assert game_fixture.guess_letter == "a"
    assert game_fixture.current_word == "____"
    assert game_fixture.errors == ["a"]
    assert game_fixture.history == [Move(1, "a", hit=False)]


def test_game_play_turn_guessed_letter(game_fixture: Game) -> None:
    """
    Test the game play turn with a guessed letter: all its occurrences are revealed.
    """
    game_fixture.start_next_turn()
    assert game_fixture.play_turn("t") == GameState.ONGOING
    assert game_fixture.guess_letter == "t"
    assert game_fixture.current_word == "t__t"
    assert game_fixture.errors == []
    assert game_fixture.history == [Move(1, "t", hit=True)]


def test_game_play_turn_regex_special_char(game_fixture: Game) -> None:
    """
    "*" is returned by the controller when input tries are exceeded; it must count as an error, not crash.
    """
    game_fixture.start_next_turn()
    game_fixture.play_turn("*")
    assert game_fixture.current_word == "____"
    assert game_fixture.errors == ["*"]


def test_game_play_turn_before_start(game_fixture: Game) -> None:
    """
    Playing a turn before start_next_turn() raises a clear error.
    """
    with pytest.raises(RuntimeError, match='Turn is not started'):
        game_fixture.play_turn("t")


def test_game_history_records_moves(game_fixture: Game) -> None:
    for letter in ["t", "a", "e", "s"]:
        game_fixture.start_next_turn()
        game_fixture.play_turn(letter)
    assert game_fixture.history == [
        Move(1, "t", hit=True),
        Move(2, "a", hit=False),
        Move(3, "e", hit=True),
        Move(4, "s", hit=True),
    ]
    assert game_fixture.state() == GameState.WON


def test_move_is_immutable() -> None:
    move = Move(1, "t", hit=True)
    with pytest.raises(AttributeError):
        move.letter = "a"  # type: ignore[misc]
