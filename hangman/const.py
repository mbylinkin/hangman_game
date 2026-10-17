"""Constants module."""

from __future__ import annotations

from enum import Enum
from pathlib import Path

# Vocabulary is package data, so it is found both in a checkout and in an installed package.
WORDS_PATH = Path(__file__).resolve().parent / 'data' / 'words.txt'
MAX_GUESS_ERRORS = 6
MAX_LETTER_INPUT_TRIES = 3


class GameState(Enum):
    """Game states."""

    ONGOING = "Ongoing"
    WON = "Won"
    LOST = "Lost"
