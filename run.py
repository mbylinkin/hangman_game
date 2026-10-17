from __future__ import annotations

from app.const import WORDS_PATH
from app.input import WordVocabulary
from app.main import GameApplication


def main():
    vocabulary = WordVocabulary(WORDS_PATH)
    game = GameApplication(vocabulary)
    game.loop()


if __name__ == '__main__':
    main()
