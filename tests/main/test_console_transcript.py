from __future__ import annotations

import random
from pathlib import Path

import pytest
from pytest_mock.plugin import MockerFixture

from app import cli

TRANSCRIPT_PATH = Path(__file__).resolve().parent.parent / 'data' / 'console_transcript.txt'

# Two games with a fixed seed: invalid inputs and exceeded tries, a win, "Y" for a new game, a loss, quit.
PLAYER_INPUT = 'y 11 aa e e 1 22 333 a i o u s t r n l c d Y q x z j v k w'.split()


def test_console_output_matches_transcript(mocker: MockerFixture, capsys: pytest.CaptureFixture[str]) -> None:
    """
    Whole console game output, byte for byte. Update the transcript only for intended output changes.
    """
    answers = iter(PLAYER_INPUT)

    def fake_input(prompt: str = '') -> str:
        print(prompt, end='')
        return next(answers)

    mocker.patch('app.input.random', random.Random(42))
    mocker.patch('builtins.input', side_effect=fake_input)
    cli.main([])
    assert next(answers, None) is None, 'not all player input was used'
    assert capsys.readouterr().out == TRANSCRIPT_PATH.read_text(encoding='utf-8')
