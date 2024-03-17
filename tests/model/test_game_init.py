from __future__ import annotations

import pytest

from app.model import Game


def test_init_valid_inputs() -> None:
    """
    Function to test the initialization with valid inputs.
    """
    secret_word = "test"
    instance = Game(secret_word)
    assert instance.secret_word == secret_word
    assert instance.current_word == "____"
    assert instance.errors == []
    assert instance.current_turn is None
    assert instance.turn_history == []


def test_init_invalid_inputs() -> None:
    """
    A function to test invalid inputs for the initialization of the test class.
    """
    secret_word = 123  # invalid input
    with pytest.raises(TypeError):
        Game(secret_word)  # type: ignore
