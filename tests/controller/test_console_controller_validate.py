from __future__ import annotations

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


def test_valid_lowercase_letter(controller_fixture: ConsoleGameController) -> None:
    guess_letter = "a"
    validate_result, _ = controller_fixture.validate_letter(guess_letter)
    assert validate_result


def test_invalid_input_not_single_letter(
    controller_fixture: ConsoleGameController,
) -> None:
    guess_letter = "ab"
    validate_result, _ = controller_fixture.validate_letter(guess_letter)
    assert not validate_result


def test_invalid_input_not_a_letter(controller_fixture: ConsoleGameController) -> None:
    guess_letter = "1"
    validate_result, _ = controller_fixture.validate_letter(guess_letter)
    assert not validate_result
