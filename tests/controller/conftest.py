from __future__ import annotations

import pytest

from app.controller import BaseGameController
from app.controller import ConsoleGameController
from tests.conftest import FakeView


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


@pytest.fixture
def fake_controller(fake_view: FakeView) -> BaseGameController:
    """
    Fixture for the game controller with a fake view and a started game, secret word "test".
    """
    controller = BaseGameController(fake_view)
    controller.start_game("test")
    return controller
