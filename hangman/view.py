from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from hangman import templates
from hangman.const import GameState
from hangman.model import Game


class BaseView(ABC):
    """
    Base view: all user input and output of the game goes through it.
    A subclass must implement every method, otherwise it cannot be instantiated.
    """

    @abstractmethod
    def render(self, current_game: Game) -> None:
        """Show the current turn and, when the game is over, its result."""

    @abstractmethod
    def ask_new_game(self) -> bool:
        """Ask the player whether to start a new game."""

    @abstractmethod
    def ask_letter(self) -> str:
        """Ask the player for a letter; the input is returned as is, without validation."""

    @abstractmethod
    def show_message(self, message: str) -> None:
        """Show a message to the player, e.g. why the input is not accepted."""


class ConsoleView(BaseView):
    """Console renderer."""

    def ask_new_game(self) -> bool:
        return input('Start new game? (y/n):').lower() == 'y'

    def ask_letter(self) -> str:
        return input("Input letter:")

    def show_message(self, message: str) -> None:
        print(message)

    def render(self, current_game: Game) -> None:
        if current_game.turn_number > 0:
            self.render_turn(current_game)
        if current_game.state() != GameState.ONGOING:
            self.render_game_over(current_game)

    def render_turn(self, current_game: Game) -> None:
        errors_count = len(current_game.errors)
        rendered_template = templates.template_round.format(
            round=current_game.turn_number,
            secret_word=current_game.secret_word,
            current_word=current_game.current_word,
            errors=','.join(current_game.errors),
            letter=current_game.guess_letter,
            head=templates.head_ascii[errors_count],
            body=templates.body_ascii[errors_count],
            legs=templates.legs_ascii[errors_count],
        )
        print(rendered_template)

    def render_game_over(self, current_game: Game) -> None:
        result = 'YOU LOSE :(' if current_game.state() == GameState.LOST else 'YOU WIN :)'
        rendered_template = templates.template_game_over.format(
            message=result,
            round=current_game.turn_number,
            secret_word=current_game.secret_word.upper(),
            current_word=current_game.current_word,
        )

        print(rendered_template)
