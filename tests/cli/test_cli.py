from __future__ import annotations

import runpy
import sys
from collections.abc import Callable
from pathlib import Path

import pytest
from pytest_mock.plugin import MockerFixture

from hangman import cli
from hangman.const import WORDS_PATH

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def test_console_by_default(mocker: MockerFixture) -> None:
    loop = mocker.patch('hangman.cli.GameApplication.loop')
    cli.main([])
    loop.assert_called_once()


def test_console_does_not_import_tkinter(mocker: MockerFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    The console game must work on Python builds without tkinter.
    """
    mocker.patch('hangman.cli.GameApplication.loop')
    monkeypatch.delitem(sys.modules, 'hangman.gui', raising=False)
    monkeypatch.setitem(sys.modules, 'tkinter', None)  # makes `import tkinter` fail
    cli.main([])
    assert 'hangman.gui' not in sys.modules


def test_gui_flag_runs_gui(mocker: MockerFixture) -> None:
    pytest.importorskip('tkinter')
    run_gui = mocker.patch('hangman.gui.run_gui')
    loop = mocker.patch('hangman.cli.GameApplication.loop')
    cli.main(['--gui'])
    run_gui.assert_called_once()
    loop.assert_not_called()


def test_unknown_argument_exits() -> None:
    with pytest.raises(SystemExit):
        cli.main(['--unknown'])


@pytest.mark.parametrize(
    'run',
    [
        lambda: runpy.run_module('hangman', run_name='__main__'),
        lambda: runpy.run_path(str(REPO_ROOT / 'run.py'), run_name='__main__'),
    ],
    ids=['python_-m_app', 'run.py'],
)
def test_entry_points_call_main(
    mocker: MockerFixture, monkeypatch: pytest.MonkeyPatch, run: Callable[[], object]
) -> None:
    monkeypatch.setattr(sys, 'argv', ['hangman'])
    loop = mocker.patch('hangman.cli.GameApplication.loop')
    run()
    loop.assert_called_once()


def test_words_file_is_package_data() -> None:
    """
    The vocabulary must live inside the package, otherwise an installed game cannot find it.
    """
    assert WORDS_PATH.parent.parent == Path(cli.__file__).resolve().parent
    assert WORDS_PATH.is_file()
