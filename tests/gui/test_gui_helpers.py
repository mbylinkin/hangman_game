from __future__ import annotations

import pytest

pytest.importorskip('tkinter')

from app.const import MAX_GUESS_ERRORS  # noqa: E402
from app.gui import format_word  # noqa: E402
from app.gui import game_result_text  # noqa: E402
from app.gui import HANGMAN_PARTS  # noqa: E402
from app.gui import hangman_parts  # noqa: E402
from app.model import Game  # noqa: E402


def test_one_part_per_error_up_to_max() -> None:
    assert len(HANGMAN_PARTS) == MAX_GUESS_ERRORS
    assert hangman_parts(0) == ()
    assert hangman_parts(1) == ('head',)
    assert hangman_parts(4) == ('head', 'body', 'left_arm', 'right_arm')
    assert hangman_parts(MAX_GUESS_ERRORS) == HANGMAN_PARTS


def test_format_word() -> None:
    assert format_word('t__t') == 'T _ _ T'


def test_game_result_text() -> None:
    game = Game('t')
    game.start_next_turn()
    game.play_turn('t')
    assert game_result_text(game) == 'YOU WIN :)  Secret word: T'
    game = Game('t')
    for letter in 'abcdef'[:MAX_GUESS_ERRORS]:
        game.start_next_turn()
        game.play_turn(letter)
    assert game_result_text(game) == 'YOU LOSE :(  Secret word: T'
