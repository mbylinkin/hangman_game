from __future__ import annotations

import pytest
from pytest_mock.plugin import MockerFixture

pytest.importorskip('tkinter')


from app.const import GameState  # noqa: E402
from app.controller import BaseGameController  # noqa: E402
from app.gui import GameClosed  # noqa: E402
from app.gui import run_gui  # noqa: E402
from app.gui import TkView  # noqa: E402
from app.input import WordVocabulary  # noqa: E402
from app.main import GameApplication  # noqa: E402
from app.model import Game  # noqa: E402
from tests.gui.conftest import autoplay  # noqa: E402
from tests.gui.conftest import window_exists  # noqa: E402


def test_ask_letter_from_button(tk_view: TkView) -> None:
    tk_view.root.after(5, lambda: tk_view.letter_buttons['t'].invoke())
    assert tk_view.ask_letter() == 't'
    assert not tk_view.waiting
    assert tk_view.letter_buttons['t']['state'] == 'disabled'


def test_ask_letter_from_keyboard(tk_view: TkView) -> None:
    tk_view.root.after(5, lambda: tk_view.press_key('E'))
    assert tk_view.ask_letter() == 'E'


def test_press_key_ignored_when_not_waiting(tk_view: TkView) -> None:
    tk_view.press_key('a')
    tk_view.root.after(5, lambda: tk_view.press_key('b'))
    assert tk_view.ask_letter() == 'b'


@pytest.mark.parametrize('char', ['1', '', 'ab', ' '])
def test_press_key_ignores_non_letters(tk_view: TkView, char: str) -> None:
    def press() -> None:
        tk_view.press_key(char)
        tk_view.press_key('z')

    tk_view.root.after(5, press)
    assert tk_view.ask_letter() == 'z'


def test_used_letters_disabled_while_waiting(tk_view: TkView) -> None:
    game = Game('test')
    game.start_next_turn()
    game.play_turn('t')
    game.start_next_turn()
    game.play_turn('a')
    tk_view.render(game)
    states: dict[str, str] = {}

    def check_and_press() -> None:
        states.update({letter: tk_view.letter_buttons[letter]['state'] for letter in 'tab'})
        tk_view.press_key('b')

    tk_view.root.after(5, check_and_press)
    tk_view.ask_letter()
    assert states == {'t': 'disabled', 'a': 'disabled', 'b': 'normal'}


def test_close_while_waiting_raises_game_closed(tk_view: TkView) -> None:
    tk_view.root.after(5, tk_view.close)
    with pytest.raises(GameClosed):
        tk_view.ask_letter()
    assert tk_view.closed
    with pytest.raises(GameClosed):
        tk_view.ask_letter()


def test_close_when_not_waiting_destroys_window(tk_view: TkView) -> None:
    tk_view.close()
    assert not window_exists(tk_view.root)
    assert tk_view.ask_new_game() is False


@pytest.mark.parametrize('answer', [True, False])
def test_ask_new_game(tk_view: TkView, mocker: MockerFixture, answer: bool) -> None:
    askyesno = mocker.patch('app.gui.messagebox.askyesno', return_value=answer)
    assert tk_view.ask_new_game() is answer
    askyesno.assert_called_once()


def test_show_message(tk_view: TkView) -> None:
    tk_view.show_message('Your input is not a letter. Try again.')
    assert tk_view.message_label['text'] == 'Your input is not a letter. Try again.'


def test_render_ongoing_game(tk_view: TkView) -> None:
    game = Game('test')
    game.start_next_turn()
    game.play_turn('t')
    game.start_next_turn()
    game.play_turn('a')
    tk_view.show_message('old message')
    tk_view.render(game)
    assert tk_view.round_label['text'] == 'Round 2'
    assert tk_view.word_label['text'] == 'T _ _ T'
    assert tk_view.errors_label['text'] == 'Errors: a'
    assert len(tk_view.canvas.find_withtag('part')) == 1
    assert tk_view.message_label['text'] == ''


def test_render_game_over(tk_view: TkView) -> None:
    game = Game('o')
    for letter in 'abcdef':
        game.start_next_turn()
        game.play_turn(letter)
    tk_view.render(game)
    assert len(tk_view.canvas.find_withtag('part')) == 6
    assert tk_view.message_label['text'] == 'YOU LOSE :(  Secret word: O'


def test_full_game_in_window(tk_view: TkView, mocker: MockerFixture) -> None:
    """
    The whole application runs with the window view: one won game, then the player declines a new one.
    """
    mocker.patch('app.input.read_words_from_file', return_value=['test'])
    mocker.patch('app.gui.messagebox.askyesno', side_effect=[True, False])
    controller = BaseGameController(tk_view)
    application = GameApplication(WordVocabulary('words.txt'), controller=controller)
    autoplay(tk_view, ['x', 'X', 't', 'e', 's'])
    application.loop()
    assert controller.game.state() == GameState.WON
    assert controller.game.errors == ['x']
    assert tk_view.message_label['text'] == 'YOU WIN :)  Secret word: TEST'


def test_run_gui_returns_when_window_closed(tk_view: TkView, mocker: MockerFixture) -> None:
    mocker.patch('app.input.read_words_from_file', return_value=['test'])
    mocker.patch('app.gui.messagebox.askyesno', return_value=True)
    tk_view.root.after(20, tk_view.close)
    run_gui(WordVocabulary('words.txt'), view=tk_view)
    assert tk_view.closed


def test_run_gui_destroys_window_when_player_quits(tk_view: TkView, mocker: MockerFixture) -> None:
    mocker.patch('app.input.read_words_from_file', return_value=['test'])
    mocker.patch('app.gui.messagebox.askyesno', return_value=False)
    run_gui(WordVocabulary('words.txt'), view=tk_view)
    assert not window_exists(tk_view.root)
