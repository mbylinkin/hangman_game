from __future__ import annotations

from unittest import mock

import pytest

from hangman.model import Game
from hangman.view import ConsoleView


@pytest.mark.parametrize(
    ("answer", "expected"),
    [("y", True), ("Y", True), ("n", False), ("", False), ("yes", False)],
)
def test_ask_new_game(answer: str, expected: bool) -> None:
    with mock.patch("builtins.input", return_value=answer) as input_mock:
        assert ConsoleView().ask_new_game() is expected
    input_mock.assert_called_once_with('Start new game? (y/n):')


def test_ask_letter_returns_raw_input() -> None:
    with mock.patch("builtins.input", return_value="A ") as input_mock:
        assert ConsoleView().ask_letter() == "A "
    input_mock.assert_called_once_with("Input letter:")


def test_show_message(capsys: pytest.CaptureFixture[str]) -> None:
    ConsoleView().show_message("Hello")
    assert capsys.readouterr().out == "Hello\n"


def test_render_turn_and_game_over(capsys: pytest.CaptureFixture[str]) -> None:
    game = Game("t")
    game.start_next_turn()
    game.play_turn("t")
    ConsoleView().render(game)
    out = capsys.readouterr().out
    assert "Round:1" in out
    assert "YOU WIN :)" in out
    assert "Secret word:  T" in out


def test_render_ongoing_game_without_game_over(capsys: pytest.CaptureFixture[str]) -> None:
    game = Game("test")
    game.start_next_turn()
    ConsoleView().render(game)
    out = capsys.readouterr().out
    assert "Round:1" in out
    assert "GAME OVER" not in out
