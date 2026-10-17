from __future__ import annotations

from unittest import mock

import pytest
from pytest_mock.plugin import MockerFixture

from app import controller
from app.const import GameState
from app.input import WordVocabulary
from app.main import GameApplication


@pytest.fixture
def game_app_fixture(mocker: MockerFixture) -> GameApplication:
    """
    Game application with a vocabulary of a single word "test".
    """
    mocker.patch('app.input.read_words_from_file', return_value=['test'])
    return GameApplication(WordVocabulary('words.txt'))


def test_game_controller_init(game_app_fixture: GameApplication) -> None:
    app = game_app_fixture
    assert isinstance(app.controller, controller.ConsoleGameController)
    assert isinstance(app.vocabulary, WordVocabulary)


def test_game_controller_play_game_player_1_wins(game_app_fixture: GameApplication) -> None:
    with mock.patch(
        "builtins.input",
        side_effect=["u", "e", "s", "d", "f", "k", "l", "i"],
    ):
        game_app_fixture.play_game()
    current_game = game_app_fixture.controller.current_game
    assert current_game.state() == GameState.PLAYER_1_WINS
    assert current_game.current_turn.turn_number == 8
    assert current_game.current_turn.secret_word == "test"
    assert current_game.current_turn.current_word == "_es_"
    assert current_game.current_turn.errors == ["u", "d", "f", "k", "l", "i"]


def test_game_controller_play_game_player_2_wins(game_app_fixture: GameApplication) -> None:
    with mock.patch("builtins.input", side_effect=["t", "e", "s"]):
        game_app_fixture.play_game()
    current_game = game_app_fixture.controller.current_game
    assert current_game.state() == GameState.PLAYER_2_WINS
    assert current_game.current_turn.turn_number == 3
    assert current_game.current_turn.current_word == "test"
    assert current_game.current_turn.errors == []


def test_game_controller_play_game_input_tries_exceeded(game_app_fixture: GameApplication) -> None:
    with mock.patch("builtins.input", side_effect=["11", "22", "33", "t", "e", "s"]):
        game_app_fixture.play_game()
    current_game = game_app_fixture.controller.current_game
    assert current_game.current_turn.current_word == "test"
    assert current_game.current_turn.errors == ["*"]


@pytest.mark.parametrize(
    ("answers", "games_played"),
    [
        (["n"], 0),
        ([""], 0),
        (["y", "n"], 1),
        (["Y", "y", "no"], 2),
    ],
)
def test_loop_plays_until_not_yes(
    game_app_fixture: GameApplication,
    mocker: MockerFixture,
    answers: list[str],
    games_played: int,
) -> None:
    play_game_mock = mocker.patch.object(game_app_fixture, 'play_game')
    with mock.patch("builtins.input", side_effect=answers):
        game_app_fixture.loop()
    assert play_game_mock.call_count == games_played
