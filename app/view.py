from __future__ import annotations

from typing import Protocol

from jinja2 import Template

from app import templates
from app.const import GameState
from app.model import Game


class GameTurnProtocol(Protocol):
    turn_number: int
    secret_word: str
    current_word: str
    errors: list[str]
    guess_letter: str


class BaseView:
    """Base view."""

    def render(self, current_game: Game) -> None:
        raise NotImplementedError


class ConsoleView(BaseView):
    """Console renderer."""

    def render(self, current_game: Game) -> None:
        if game_turn := current_game.get_current_turn():
            self.render_turn(game_turn)
        if current_game.state() != GameState.ONGOING:
            self.render_game_over(current_game)

    def render_turn(self, game_turn: GameTurnProtocol) -> None:
        template_text = templates.template_round
        template = Template(template_text)
        rendered_template = template.render(
            round=game_turn.turn_number,
            secret_word=game_turn.secret_word,
            current_word=game_turn.current_word,
            errors=','.join(game_turn.errors),
            letter=game_turn.guess_letter,
            head=templates.head_ascii[len(game_turn.errors)],
            body=templates.body_ascii[len(game_turn.errors)],
            legs=templates.legs_ascii[len(game_turn.errors)],
        )
        print(rendered_template)

    def render_game_over(self, current_game: Game) -> None:
        result = 'YOU LOSE :(' if current_game.state() == GameState.PLAYER_1_WINS else 'YOU WIN :)'
        template_text = templates.template_game_over
        template = Template(template_text)
        rendered_template = template.render(
            message=result,
            round=current_game.current_turn.turn_number,
            secret_word=current_game.secret_word.upper(),
            current_word=current_game.current_word,
        )

        print(rendered_template)
