from __future__ import annotations

from unittest import mock
from unittest.mock import Mock

import pytest

from app import controller
from app.input import WordVocabulary
from app.main import GameApplication


def mock_random_word(*args, **kwargs):
    return "test"


@pytest.fixture
def game_app_fixture(monkeypatch) -> GameApplication:
    monkeypatch.setattr(WordVocabulary, "random_word", mock_random_word)
    mock.patch("app.controller.ConsoleGameController.render", return_value=Mock())
    _game_app = GameApplication(WordVocabulary("data/words.txt"))
    return _game_app


def test_game_controller_init(game_app_fixture) -> None:
    app = game_app_fixture
    assert app.vocabulary is not None
    assert app.controller is not None
    assert isinstance(app.controller, controller.ConsoleGameController)
    assert isinstance(app.vocabulary, WordVocabulary)


def test_game_controller_play_game_player_1_wins(monkeypatch, game_app_fixture) -> None:
    with mock.patch(
        "builtins.input",
        side_effect=["u", "e", "s", "d", "f", "k", "l", "i"],
    ):
        game_app_fixture.play_game()
        assert game_app_fixture.controller.current_game.current_turn is not None
        assert game_app_fixture.controller.current_game.current_turn.turn_number == 8
        assert game_app_fixture.controller.current_game.current_turn.secret_word == "test"
        assert game_app_fixture.controller.current_game.current_turn.current_word == "_es_"
        assert game_app_fixture.controller.current_game.current_turn.errors == [
            "u",
            "d",
            "f",
            "k",
            "l",
            "i",
        ]


def test_game_controller_play_game_player_2_wins(monkeypatch, game_app_fixture) -> None:
    with mock.patch("builtins.input", side_effect=["t", "e", "s", "t"]):
        game_app_fixture.play_game()
        assert game_app_fixture.controller.current_game.current_turn is not None
        assert game_app_fixture.controller.current_game.current_turn.turn_number == 3
        assert game_app_fixture.controller.current_game.current_turn.secret_word == "test"
        assert game_app_fixture.controller.current_game.current_turn.current_word == "test"
        assert game_app_fixture.controller.current_game.current_turn.errors == []
