from __future__ import annotations

import pytest

from hangman.controller import BaseGameController
from tests.conftest import FakeView


@pytest.mark.parametrize(
    ("letters", "expected", "messages"),
    [
        (["a"], "a", []),
        (["aa", "a"], "a", ["Your input is not a single letter. Try again."]),
        (
            ["aa", "1", "b"],
            "b",
            ["Your input is not a single letter. Try again.", "Your input is not a letter. Try again."],
        ),
        (["A"], "a", []),
    ],
    ids=["valid_1st_try", "valid_2nd_try", "valid_3rd_try", "uppercase_lowered"],
)
def test_input_letter_valid(
    fake_controller: BaseGameController,
    fake_view: FakeView,
    letters: list[str],
    expected: str,
    messages: list[str],
) -> None:
    fake_view.letters = letters
    assert fake_controller.input_letter() == expected
    assert fake_view.messages == messages
    assert fake_view.letters == []


def test_input_letter_tries_exceeded(fake_controller: BaseGameController, fake_view: FakeView) -> None:
    fake_view.letters = ["aa", "ab", "bc", "c"]
    assert fake_controller.input_letter() == "*"
    assert fake_view.letters == ["c"]
    assert fake_view.messages[-1] == "Number of tries exceeded."
    assert len(fake_view.messages) == fake_controller.max_input_tries + 1


def test_input_letter_in_errors(fake_controller: BaseGameController, fake_view: FakeView) -> None:
    fake_controller.game.errors = ["a"]
    fake_view.letters = ["a", "ab", "bc"]
    assert fake_controller.input_letter() == "*"
    assert fake_view.messages[0] == "You already guessed this letter. Try again."


@pytest.mark.parametrize("answer", [True, False])
def test_ask_new_game_delegates_to_view(
    fake_controller: BaseGameController,
    fake_view: FakeView,
    answer: bool,
) -> None:
    fake_view.new_game_answers = [answer]
    assert fake_controller.ask_new_game() is answer
