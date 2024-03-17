from __future__ import annotations

import random


def read_words_from_file(path: str) -> list:
    """
    Read words from a file and return them as a list.

    Args:
        path (str): Path to the file.

    Returns:
        list: List of words.
    """
    with open(path) as file:
        return file.read().splitlines()


class WordVocabulary:
    """Holds a list of words and provides a random word."""

    def __init__(self, path: str) -> None:
        self.words = read_words_from_file(path) or []
        self.used_words: list[int] = []

    def random_idx(self) -> int:
        """
        Get a random index of a word from the vocabulary.

        Returns:
            int: Random index of a word.
        """
        random_idx = random.randint(0, len(self.words) - 1)
        while random_idx in self.used_words:
            random_idx = random.randint(0, len(self.words) - 1)
        self.used_words.append(random_idx)
        return random_idx

    def random_word(self) -> str:
        """
        Generate a random word from the list of words and return it.
        """
        idx = self.random_idx()
        return self.words[idx]
