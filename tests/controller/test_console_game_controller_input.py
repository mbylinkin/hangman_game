from __future__ import annotations

from unittest import mock

import pytest

from app.controller import ConsoleGameController


@pytest.fixture
def controller_fixture() -> ConsoleGameController:
    """
    Fixture for the game controller with a secret word, returning a ConsoleGameController object.
    """
    controller = ConsoleGameController()
    controller.start_game("test")
    return controller


def test_input_letter_1_time_right(controller_fixture: ConsoleGameController) -> None:
    with mock.patch("builtins.input", side_effect=["a", "sa", "a", "e"]):
        input_result = controller_fixture.input_letter()
        assert input_result == "a"


def test_input_letter_2_time_valid(controller_fixture: ConsoleGameController) -> None:
    with mock.patch("builtins.input", side_effect=["aa", "a", "b", "c"]):
        input_result = controller_fixture.input_letter()
        assert input_result == "a"


def test_input_letter_3_time_valid(controller_fixture: ConsoleGameController) -> None:
    with mock.patch("builtins.input", side_effect=["aa", "ab", "b", "c"]):
        input_result = controller_fixture.input_letter()
        assert input_result == "b"


def test_input_letter_no_valid(controller_fixture: ConsoleGameController) -> None:
    with mock.patch("builtins.input", side_effect=["aa", "ab", "bc", "c"]):
        input_result = controller_fixture.input_letter()
        assert input_result == "*"


def test_input_letter_in_erorrs(controller_fixture: ConsoleGameController) -> None:
    with mock.patch("builtins.input", side_effect=["a", "ab", "bc", "c"]):
        controller_fixture.current_game.errors = ["a"]
        input_result = controller_fixture.input_letter()
        print(input_result)
        assert input_result == "*"
