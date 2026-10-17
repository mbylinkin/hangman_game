from __future__ import annotations

from jinja2 import Template

from app import templates
from app.const import GameState
from app.model import Game


class BaseView:
    """Base view: all user input and output of the game goes through it."""

    def render(self, current_game: Game) -> None:
        raise NotImplementedError

    def ask_new_game(self) -> bool:
        """Ask the player whether to start a new game."""
        raise NotImplementedError

    def ask_letter(self) -> str:
        """Ask the player for a letter; the input is returned as is, without validation."""
        raise NotImplementedError

    def show_message(self, message: str) -> None:
        raise NotImplementedError


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
        template_text = templates.template_round
        template = Template(template_text)
        errors_count = len(current_game.errors)
        rendered_template = template.render(
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
        template_text = templates.template_game_over
        template = Template(template_text)
        rendered_template = template.render(
            message=result,
            round=current_game.turn_number,
            secret_word=current_game.secret_word.upper(),
            current_word=current_game.current_word,
        )

        print(rendered_template)
