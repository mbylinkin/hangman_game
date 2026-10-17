from __future__ import annotations

import pytest

from hangman.model import Game


def test_init_valid_inputs() -> None:
    """
    Function to test the initialization with valid inputs.
    """
    secret_word = "test"
    instance = Game(secret_word)
    assert instance.secret_word == secret_word
    assert instance.current_word == "____"
    assert instance.errors == []
    assert instance.guessed == set()
    assert instance.turn_number == 0
    assert instance.guess_letter == ""
    assert instance.history == []


def test_init_invalid_inputs() -> None:
    """
    A function to test invalid inputs for the initialization of the test class.
    """
    secret_word = 123  # invalid input
    with pytest.raises(TypeError):
        Game(secret_word)  # type: ignore[arg-type]
