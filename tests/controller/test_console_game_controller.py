from __future__ import annotations

import pytest

from hangman.const import GameState
from hangman.const import MAX_GUESS_ERRORS
from hangman.controller import ConsoleGameController
from hangman.model import Game
from hangman.view import ConsoleView


def test_game_controller_init(controller: ConsoleGameController) -> None:
    assert controller.current_game is None
    assert isinstance(controller.view, ConsoleView)


def test_game_controller_start_game(controller: ConsoleGameController) -> None:
    controller.start_game("test")
    assert isinstance(controller.current_game, Game)
    assert controller.game.secret_word == "test"


def test_game_controller_play_turn(started_controller: ConsoleGameController) -> None:
    started_controller.start_next_turn()
    game_state = started_controller.play_turn("t")
    game = started_controller.game
    assert game_state == GameState.ONGOING
    assert game.secret_word == "test"
    assert game.current_word == "t__t"
    assert game.errors == []


def test_game_controller_game_state_at_start(started_controller: ConsoleGameController) -> None:
    assert started_controller.game_pending()


def test_game_controller_game_state_after_turn(started_controller: ConsoleGameController) -> None:
    started_controller.start_next_turn()
    started_controller.play_turn("t")
    assert started_controller.game_pending()


def test_game_controller_game_state_after_end_lost(controller: ConsoleGameController) -> None:
    controller.start_game("o")
    for letter in "abcdefghijklmn"[:MAX_GUESS_ERRORS]:
        assert controller.game_pending()
        controller.start_next_turn()
        controller.play_turn(letter)
    assert not controller.game_pending()
    assert controller.game_state() == GameState.LOST


def test_game_controller_game_state_after_end_won(controller: ConsoleGameController) -> None:
    controller.start_game("t")
    controller.start_next_turn()
    controller.play_turn("t")
    assert not controller.game_pending()
    assert controller.game_state() == GameState.WON


def test_game_controller_game_not_started(controller: ConsoleGameController) -> None:
    with pytest.raises(RuntimeError, match='Game is not started'):
        controller.game_pending()
