from __future__ import annotations

import sys

import pytest
from pytest_mock.plugin import MockerFixture

import run


def test_console_by_default(mocker: MockerFixture) -> None:
    loop = mocker.patch('run.GameApplication.loop')
    run.main([])
    loop.assert_called_once()


def test_console_does_not_import_tkinter(mocker: MockerFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    The console game must work on Python builds without tkinter.
    """
    mocker.patch('run.GameApplication.loop')
    monkeypatch.delitem(sys.modules, 'app.gui', raising=False)
    monkeypatch.setitem(sys.modules, 'tkinter', None)  # makes `import tkinter` fail
    run.main([])
    assert 'app.gui' not in sys.modules


def test_gui_flag_runs_gui(mocker: MockerFixture) -> None:
    pytest.importorskip('tkinter')
    run_gui = mocker.patch('app.gui.run_gui')
    loop = mocker.patch('run.GameApplication.loop')
    run.main(['--gui'])
    run_gui.assert_called_once()
    loop.assert_not_called()


def test_unknown_argument_exits() -> None:
    with pytest.raises(SystemExit):
        run.main(['--unknown'])
