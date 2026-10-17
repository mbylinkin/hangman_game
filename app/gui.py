"""Tkinter GUI: a BaseView implementation that shows the game in a window."""

from __future__ import annotations

import string
import tkinter as tk
from functools import partial
from tkinter import messagebox

from app.const import GameState
from app.controller import BaseGameController
from app.input import WordVocabulary
from app.main import GameApplication
from app.model import Game
from app.view import BaseView

# Hangman parts in the order they appear, one per error (same stages as the ASCII templates).
HANGMAN_PARTS = ('head', 'body', 'left_arm', 'right_arm', 'left_leg', 'right_leg')

GALLOWS_LINES = (
    (20, 200, 140, 200),
    (50, 200, 50, 20),
    (50, 20, 130, 20),
    (130, 20, 130, 45),
)
PART_LINES = {
    'body': (130, 75, 130, 135),
    'left_arm': (130, 90, 105, 115),
    'right_arm': (130, 90, 155, 115),
    'left_leg': (130, 135, 110, 170),
    'right_leg': (130, 135, 150, 170),
}
HEAD_OVAL = (115, 45, 145, 75)


class GameClosed(Exception):
    """Raised when the window is closed while the game waits for the player."""


def hangman_parts(errors_count: int) -> tuple[str, ...]:
    """Hangman parts to draw for the given number of errors."""
    return HANGMAN_PARTS[: max(errors_count, 0)]


def format_word(current_word: str) -> str:
    """Word for display: "t__t" -> "T _ _ T"."""
    return ' '.join(current_word.upper())


def game_result_text(current_game: Game) -> str:
    result = 'YOU LOSE :(' if current_game.state() == GameState.LOST else 'YOU WIN :)'
    return f'{result}  Secret word: {current_game.secret_word.upper()}'


class TkView(BaseView):
    """
    Window view. ask_letter() waits for a letter with wait_variable(), which processes window
    events until the player presses a letter button or a key, so the controller can ask for
    input the same way as in the console.
    """

    def __init__(self, root: tk.Tk | tk.Toplevel | None = None) -> None:
        """root: the window to build the view in; a new Tk window by default."""
        self.root: tk.Tk | tk.Toplevel = root or tk.Tk()
        self.root.title('Hangman')
        self.root.resizable(False, False)
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        self.root.bind('<Key>', lambda event: self.press_key(event.char))

        self.closed = False
        self.waiting = False
        self.used_letters: set[str] = set()
        self._letter = tk.StringVar(self.root)

        self.round_label = tk.Label(self.root, font=('Helvetica', 12))
        self.round_label.grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=(10, 0))
        self.canvas = tk.Canvas(self.root, width=180, height=210, highlightthickness=0)
        self.canvas.grid(row=1, column=0, rowspan=2, padx=10)
        for line in GALLOWS_LINES:
            self.canvas.create_line(*line, width=3)
        self.word_label = tk.Label(self.root, font=('Courier', 24, 'bold'))
        self.word_label.grid(row=1, column=1, padx=10)
        self.errors_label = tk.Label(self.root, font=('Helvetica', 12))
        self.errors_label.grid(row=2, column=1, padx=10)
        self.message_label = tk.Label(self.root, font=('Helvetica', 12), fg='firebrick')
        self.message_label.grid(row=3, column=0, columnspan=2, pady=5)

        letters_frame = tk.Frame(self.root)
        letters_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=(0, 10))
        self.letter_buttons: dict[str, tk.Button] = {}
        for idx, letter in enumerate(string.ascii_lowercase):
            button = tk.Button(
                letters_frame,
                text=letter.upper(),
                width=3,
                state='disabled',
                command=partial(self.press_key, letter),
            )
            button.grid(row=idx // 13, column=idx % 13, padx=1, pady=1)
            self.letter_buttons[letter] = button

    def render(self, current_game: Game) -> None:
        self.used_letters = set(current_game.errors) | current_game.guessed
        self.round_label.config(text=f'Round {current_game.turn_number}' if current_game.turn_number else '')
        self.word_label.config(text=format_word(current_game.current_word))
        self.errors_label.config(text=f'Errors: {", ".join(current_game.errors)}')
        self.canvas.delete('part')
        for part in hangman_parts(len(current_game.errors)):
            if part == 'head':
                self.canvas.create_oval(*HEAD_OVAL, width=3, tags='part')
            else:
                self.canvas.create_line(*PART_LINES[part], width=3, tags='part')
        game_over = current_game.state() != GameState.ONGOING
        self.message_label.config(text=game_result_text(current_game) if game_over else '')

    def ask_new_game(self) -> bool:
        if self.closed:
            return False
        try:
            answer = messagebox.askyesno('Hangman', 'Start new game?', parent=self.root)
        except tk.TclError:  # the window was destroyed while the dialog was open
            return False
        return bool(answer) and not self.closed

    def ask_letter(self) -> str:
        if self.closed:
            raise GameClosed()
        self._set_waiting(True)
        self.root.wait_variable(self._letter)
        if self.closed:
            self.destroy()
            raise GameClosed()
        self._set_waiting(False)
        return self._letter.get()

    def show_message(self, message: str) -> None:
        self.message_label.config(text=message)

    def press_key(self, char: str) -> None:
        """Submit a letter from a button or the keyboard; ignored unless the game waits for a letter."""
        if self.waiting and len(char) == 1 and char.isalpha():
            self._letter.set(char)

    def close(self) -> None:
        """Window close button: stop waiting for the player and destroy the window."""
        self.closed = True
        if self.waiting:
            self._letter.set('')  # wakes ask_letter(), which destroys the window and raises GameClosed
        else:
            self.destroy()

    def destroy(self) -> None:
        try:
            self.root.destroy()
        except tk.TclError:  # already destroyed
            pass

    def _set_waiting(self, waiting: bool) -> None:
        self.waiting = waiting
        for letter, button in self.letter_buttons.items():
            enabled = waiting and letter not in self.used_letters
            button.config(state='normal' if enabled else 'disabled')


def run_gui(vocabulary: WordVocabulary, view: TkView | None = None) -> None:
    """Play the game in a window until the player declines a new game or closes the window."""
    view = view or TkView()
    application = GameApplication(vocabulary, controller=BaseGameController(view))
    try:
        application.loop()
    except GameClosed:
        return
    view.destroy()
