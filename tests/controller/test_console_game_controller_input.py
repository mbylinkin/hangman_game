from __future__ import annotations

from unittest import mock

import pytest

from app.controller import ConsoleGameController


@pytest.mark.parametrize(
    ("inputs", "expected"),
    [
        (["a", "sa", "a", "e"], "a"),
        (["aa", "a", "b", "c"], "a"),
        (["aa", "ab", "b", "c"], "b"),
        (["A"], "a"),
    ],
    ids=["valid_1st_try", "valid_2nd_try", "valid_3rd_try", "uppercase_lowered"],
)
def test_input_letter_valid(started_controller: ConsoleGameController, inputs: list[str], expected: str) -> None:
    with mock.patch("builtins.input", side_effect=inputs):
        assert started_controller.input_letter() == expected


def test_input_letter_tries_exceeded(started_controller: ConsoleGameController) -> None:
    with mock.patch("builtins.input", side_effect=["aa", "ab", "bc", "c"]) as input_mock:
        assert started_controller.input_letter() == "*"
    assert input_mock.call_count == started_controller.max_input_tries


def test_input_letter_in_errors(started_controller: ConsoleGameController) -> None:
    started_controller.current_game.errors = ["a"]
    with mock.patch("builtins.input", side_effect=["a", "ab", "bc", "c"]):
        assert started_controller.input_letter() == "*"
