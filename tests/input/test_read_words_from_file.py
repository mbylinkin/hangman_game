from __future__ import annotations

from pathlib import Path

from app.input import read_words_from_file


def test_read_words_lowercased(tmp_path: Path) -> None:
    words_file = tmp_path / 'words.txt'
    words_file.write_text('apple\nBible\nAmerican\n')
    assert read_words_from_file(str(words_file)) == ['apple', 'bible', 'american']


def test_read_words_skips_non_letter_words(tmp_path: Path) -> None:
    words_file = tmp_path / 'words.txt'
    words_file.write_text('apple\nAfrican-American\n\nlong-term\n  pear  \n')
    assert read_words_from_file(str(words_file)) == ['apple', 'pear']


def test_vocabulary_file_has_only_guessable_words() -> None:
    words = read_words_from_file('data/words.txt')
    assert words
    assert all(word.isalpha() and word.islower() for word in words)
