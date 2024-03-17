from __future__ import annotations

import pytest

from app.const import GameState
from app.controller import ConsoleGameController
from app.model import Game
from app.view import ConsoleView


@pytest.fixture
def controller_fixture() -> ConsoleGameController:
    controller = ConsoleGameController()
    return controller


def test_game_controller_init(controller_fixture: ConsoleGameController) -> None:
    controller = controller_fixture
    assert controller.current_game is None
    assert controller.view is not None
    assert isinstance(controller.view, ConsoleView)


def test_game_controller_start_game(controller_fixture: ConsoleGameController) -> None:
    controller = controller_fixture
    controller.start_game("test")
    assert controller.view is not None
    assert controller.current_game is not None
    assert isinstance(controller.current_game, Game)


def test_game_controller_play_turn(controller_fixture: ConsoleGameController) -> None:
    controller = controller_fixture
    controller.start_game("test")
    controller.start_next_turn()
    game_state = controller.play_turn("t")
    current_turn = controller.current_game.get_current_turn()
    assert game_state == GameState.ONGOING
    assert current_turn.secret_word == "test"
    assert current_turn.current_word == "t__t"
    assert current_turn.errors == []


def test_game_controller_game_state_at_start(
    controller_fixture: ConsoleGameController,
) -> None:
    controller = controller_fixture
    controller.start_game("test")
    assert controller.game_pending()


def test_game_controller_game_state_after_turn(
    controller_fixture: ConsoleGameController,
) -> None:
    controller = controller_fixture
    controller.start_game("test")
    controller.start_next_turn()
    _ = controller.play_turn("t")
    assert controller.game_pending()


def test_game_controller_game_state_after_end_player_1_wins(
    controller_fixture: ConsoleGameController,
) -> None:
    controller = controller_fixture
    controller.start_game("o")
    controller.start_next_turn()
    _ = controller.play_turn("t")
    assert controller.game_pending()


def test_game_controller_game_state_after_end_player_2_wins(
    controller_fixture: ConsoleGameController,
) -> None:
    controller = controller_fixture
    controller.start_game("t")
    controller.start_next_turn()
    _ = controller.play_turn("t")
    assert not controller.game_pending()
