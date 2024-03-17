from __future__ import annotations

import copy
import re

from app.const import GameState
from app.const import MAX_GUESS_ERRORS


def game_state_check(game_turn: GameTurn) -> GameState:
    """Check game state and return corresponding constant."""
    if game_turn is None:
        return GameState.ONGOING
    if len(game_turn.errors) >= MAX_GUESS_ERRORS:
        return GameState.PLAYER_1_WINS
    if game_turn.current_word.find("_") == -1:
        return GameState.PLAYER_2_WINS
    return GameState.ONGOING


class GameTurn:
    """Holds data about current game tour."""

    @classmethod
    def new_turn(cls, game_turn: GameTurn) -> GameTurn:
        return cls(
            turn_number=game_turn.turn_number + 1,
            secret_word=game_turn.secret_word,
            current_word=game_turn.current_word,
            errors=game_turn.errors,
        )

    def __init__(
        self,
        turn_number: int,
        secret_word: str,
        current_word: str,
        errors: list[str],
    ) -> None:
        self.turn_number = turn_number
        self.secret_word = secret_word
        self.current_word = current_word
        self.errors = copy.deepcopy(errors)
        self.guess_letter = ""

    def play(self, guess_letter: str) -> tuple[str, list[str]]:
        self.guess_letter = guess_letter
        occurencies = [m.start() for m in re.finditer(guess_letter, self.secret_word)]
        if len(occurencies) == 0:
            self.errors.append(guess_letter)

        for occurence in occurencies:
            self.current_word = (
                self.current_word[:occurence] + guess_letter + self.current_word[occurence + 1:]
            )  # noqa: E203

        return self.current_word, self.errors


class Game:
    """Holds data about current game."""

    def __init__(self, secret_word: str) -> None:
        self.turn_history: list[GameTurn] = []
        self.secret_word = secret_word
        self.current_word = "_" * len(secret_word)
        self.errors: list[str] = []
        self.current_turn: GameTurn = None  # type: ignore

    def start_next_turn(self) -> None:
        if self.current_turn is not None:
            self.current_turn = GameTurn.new_turn(self.current_turn)
        else:
            self.current_turn = GameTurn(
                1,
                self.secret_word,
                self.current_word,
                self.errors,
            )

    def play_turn(self, guess_letter: str) -> GameState:
        self.current_word, self.errors = self.current_turn.play(guess_letter)
        self.turn_history.append(self.current_turn)
        return self.state()

    def state(self) -> GameState:
        """
        Return the current game state.n
        """
        return game_state_check(self.current_turn)

    def get_current_turn(self) -> GameTurn:
        return self.current_turn
