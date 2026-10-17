from __future__ import annotations

from collections.abc import Iterator

import pytest

pytest.importorskip('tkinter')

import tkinter as tk  # noqa: E402

from app.gui import TkView  # noqa: E402


@pytest.fixture(scope='session')
def tk_session_root() -> Iterator[tk.Tk]:
    """
    One hidden Tk interpreter for all GUI tests: creating a Tk() per test occasionally fails on Windows
    with "Can't find a usable init.tcl". Tests are skipped when there is no display (e.g. CI without xvfb).
    """
    try:
        root = tk.Tk()
    except tk.TclError as error:
        pytest.skip(f'no display for tkinter: {error}')
    root.withdraw()
    yield root
    root.destroy()


@pytest.fixture
def tk_window(tk_session_root: tk.Tk) -> Iterator[tk.Toplevel]:
    """Hidden window for one test."""
    window = tk.Toplevel(tk_session_root)
    window.withdraw()
    yield window
    if window_exists(window):
        window.destroy()


@pytest.fixture
def tk_view(tk_window: tk.Toplevel) -> TkView:
    return TkView(tk_window)


def window_exists(window: tk.Misc) -> bool:
    try:
        return bool(window.winfo_exists())
    except tk.TclError:  # the Tk interpreter itself is destroyed
        return False


def autoplay(view: TkView, letters: list[str]) -> None:
    """
    Press the given letters one by one, each time the view waits for a letter.
    Runs on Tk timers, so it works while ask_letter() waits in wait_variable().
    """

    def step() -> None:
        if not letters or view.closed:
            return
        if view.waiting:
            view.press_key(letters.pop(0))
        view.root.after(5, step)

    view.root.after(5, step)
