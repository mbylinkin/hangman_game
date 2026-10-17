from __future__ import annotations

from dataclasses import dataclass

from hangman.const import GameState
from hangman.const import MAX_GUESS_ERRORS


def game_state_check(current_word: str, errors: list[str]) -> GameState:
    """Check game state and return corresponding constant."""
    if len(errors) >= MAX_GUESS_ERRORS:
        return GameState.LOST
    if "_" not in current_word:
        return GameState.WON
    return GameState.ONGOING


@dataclass(frozen=True)
class Move:
    """A played turn: its number, the guessed letter and whether it is in the secret word."""

    number: int
    letter: str
    hit: bool


class Game:
    """Holds the whole state of the current game."""

    def __init__(self, secret_word: str) -> None:
        if not isinstance(secret_word, str):
            raise TypeError(f'secret_word must be str, not {type(secret_word).__name__}')
        self.secret_word = secret_word
        self.guessed: set[str] = set()
        self.errors: list[str] = []
        self.turn_number = 0
        self.guess_letter = ""
        self.history: list[Move] = []

    @property
    def current_word(self) -> str:
        """Secret word with not yet guessed letters replaced by "_"."""
        return "".join(letter if letter in self.guessed else "_" for letter in self.secret_word)

    def start_next_turn(self) -> None:
        self.turn_number += 1
        self.guess_letter = ""

    def play_turn(self, guess_letter: str) -> GameState:
        if self.turn_number == 0:
            raise RuntimeError('Turn is not started, call start_next_turn() first.')
        self.guess_letter = guess_letter
        hit = guess_letter in self.secret_word
        if hit:
            self.guessed.add(guess_letter)
        else:
            self.errors.append(guess_letter)
        self.history.append(Move(self.turn_number, guess_letter, hit))
        return self.state()

    def state(self) -> GameState:
        """Return the current game state."""
        return game_state_check(self.current_word, self.errors)
