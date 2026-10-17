from __future__ import annotations

import pytest

from app.controller import ConsoleGameController


@pytest.fixture
def controller() -> ConsoleGameController:
    """
    Fixture for the game controller without a started game.
    """
    return ConsoleGameController()


@pytest.fixture
def started_controller(controller: ConsoleGameController) -> ConsoleGameController:
    """
    Fixture for the game controller with a started game, secret word "test".
    """
    controller.start_game("test")
    return controller
