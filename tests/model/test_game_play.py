from __future__ import annotations

import pytest

from app.model import Game
from app.model import GameTurn


@pytest.fixture
def game_fixture() -> Game:
    """
    Fixture for the game with a secret word and a renderer, returning a Game object.
    """
    secret_word = "test"
    game = Game(secret_word)
    return game


@pytest.fixture
def game_turn_fixture() -> GameTurn:
    """
    Fixture for generating a GameTurn object for testing.
    Returns a GameTurn object with predefined attributes.
    """
    turn_number = 1
    secret_word = "test"
    current_word = "____"
    errors: list[str] = []

    game_turn = GameTurn(turn_number, secret_word, current_word, errors)
    return game_turn


def test_game_next_turn(game_fixture: Game) -> None:
    """
    Function to test the next turn in the game.
    """
    game_fixture.start_next_turn()
    assert game_fixture.current_turn is not None
    assert game_fixture.current_turn.turn_number == 1
    assert game_fixture.current_turn.secret_word == "test"
    assert game_fixture.current_turn.current_word == "____"
    assert game_fixture.current_turn.errors == []


def test_game_play_turn_not_guessed_letter(game_fixture: Game) -> None:
    """
    Test the game play turn with letter not guessed.
    """
    guess_letter = "a"

    game_fixture.start_next_turn()
    game_fixture.play_turn(guess_letter)
    assert game_fixture.current_turn is not None
    assert game_fixture.current_turn.turn_number == 1
    assert game_fixture.current_turn.secret_word == "test"
    assert game_fixture.current_turn.current_word == "____"
    assert game_fixture.current_turn.errors == ["a"]


def test_game_play_turn_guessed_letter(game_fixture: Game) -> None:
    """
    Test the game play turn with a guessed letter.
    """
    guess_letter = "t"

    game_fixture.start_next_turn()
    game_fixture.play_turn(guess_letter)
    assert game_fixture.current_turn is not None
    assert game_fixture.current_turn.turn_number == 1
    assert game_fixture.current_turn.secret_word == "test"
    assert game_fixture.current_turn.current_word == "t__t"
    assert game_fixture.current_turn.errors == []


def test_new_game_turn(game_turn_fixture: GameTurn) -> None:
    """
    Function to test a new game turn using the given game turn fixture.
    """
    new_turn = GameTurn.new_turn(game_turn_fixture)
    assert new_turn.turn_number == 2
    assert new_turn.secret_word == "test"
    assert new_turn.current_word == "____"
    assert new_turn.errors == []


def test_game_turn_play_success(game_turn_fixture: GameTurn) -> None:
    """
    This function tests the success of playing a game turn.
    """
    game_turn_fixture.play("t")
    assert game_turn_fixture.turn_number == 1
    assert game_turn_fixture.secret_word == "test"
    assert game_turn_fixture.current_word == "t__t"
    assert game_turn_fixture.errors == []
    assert game_turn_fixture.guess_letter == "t"


def test_game_turn_play_failure(game_turn_fixture: GameTurn) -> None:
    """
    Function to test the failure scenario of playing a game turn.
    """
    game_turn_fixture.play("a")
    assert game_turn_fixture.turn_number == 1
    assert game_turn_fixture.secret_word == "test"
    assert game_turn_fixture.current_word == "____"
    assert game_turn_fixture.errors == ["a"]
    assert game_turn_fixture.guess_letter == "a"
