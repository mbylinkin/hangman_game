from __future__ import annotations

import argparse
from collections.abc import Sequence

from app.const import WORDS_PATH
from app.input import WordVocabulary
from app.main import GameApplication


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description='Hangman game')
    parser.add_argument('--gui', action='store_true', help='play in a window (tkinter) instead of the console')
    args = parser.parse_args(argv)

    vocabulary = WordVocabulary(WORDS_PATH)
    if args.gui:
        from app.gui import run_gui  # tkinter is imported only for the GUI

        run_gui(vocabulary)
    else:
        game = GameApplication(vocabulary)
        game.loop()


if __name__ == '__main__':
    main()
