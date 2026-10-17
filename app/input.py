from __future__ import annotations

import random


def read_words_from_file(path: str) -> list:
    """
    Read words from a file and return them as a list.

    Words are lowercased; words containing non-letter characters (e.g. hyphens) are skipped,
    because the player can input only letters and input is lowercased.

    Args:
        path (str): Path to the file.

    Returns:
        list: List of words.
    """
    with open(path) as file:
        words = (line.strip().lower() for line in file)
        return [word for word in words if word.isalpha()]


class WordVocabulary:
    """Holds a list of words and provides a random word."""

    def __init__(self, path: str) -> None:
        self.words = read_words_from_file(path) or []
        self.used_words: list[int] = []

    def random_idx(self) -> int:
        """
        Get a random index of a word from the vocabulary.
        When all words are used, starts over with the whole vocabulary.

        Returns:
            int: Random index of a word.
        """
        if not self.words:
            raise ValueError('Vocabulary is empty.')
        if len(self.used_words) >= len(self.words):
            self.used_words.clear()
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
