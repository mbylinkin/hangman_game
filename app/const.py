"""Constants module."""
from __future__ import annotations

from enum import Enum

MAX_GUESS_ERRORS = 6
MAX_LETTER_INPUT_TRIES = 3


class GameState(Enum):
    """Game states."""

    ONGOING = "Ongoing"
    PLAYER_1_WINS = "Player 1 wins!"
    PLAYER_2_WINS = "Player 2 wins!"
