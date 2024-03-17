from __future__ import annotations

from app.input import WordVocabulary
from app.main import GameApplication


def main():
    vocabulary = WordVocabulary('data/words.txt')
    game = GameApplication(vocabulary)
    game.loop()


if __name__ == '__main__':
    main()
