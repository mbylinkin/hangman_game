from __future__ import annotations

import pytest

from app.controller import ConsoleGameController


def test_valid_lowercase_letter(started_controller: ConsoleGameController) -> None:
    validate_result, letter = started_controller.validate_letter("a")
    assert validate_result
    assert letter == "a"


@pytest.mark.parametrize(
    ("guess_letter", "message"),
    [
        ("ab", "not a single letter"),
        ("", "not a single letter"),
        ("1", "not a letter"),
        ("*", "not a letter"),
    ],
)
def test_invalid_input(started_controller: ConsoleGameController, guess_letter: str, message: str) -> None:
    validate_result, validate_message = started_controller.validate_letter(guess_letter)
    assert not validate_result
    assert message in validate_message


def test_letter_already_in_errors(started_controller: ConsoleGameController) -> None:
    started_controller.start_next_turn()
    started_controller.play_turn("a")
    validate_result, validate_message = started_controller.validate_letter("a")
    assert not validate_result
    assert "already guessed" in validate_message


def test_letter_already_guessed(started_controller: ConsoleGameController) -> None:
    started_controller.start_next_turn()
    started_controller.play_turn("t")
    validate_result, validate_message = started_controller.validate_letter("t")
    assert not validate_result
    assert "already guessed" in validate_message
