from __future__ import annotations

from pathlib import Path

import pytest

from app.const import WORDS_PATH
from app.input import read_words_from_file


def test_read_words_lowercased(tmp_path: Path) -> None:
    words_file = tmp_path / 'words.txt'
    words_file.write_text('apple\nBible\nAmerican\n')
    assert read_words_from_file(words_file) == ['apple', 'bible', 'american']


def test_read_words_skips_non_letter_words(tmp_path: Path) -> None:
    words_file = tmp_path / 'words.txt'
    words_file.write_text('apple\nAfrican-American\n\nlong-term\n  pear  \n')
    assert read_words_from_file(words_file) == ['apple', 'pear']


def test_vocabulary_file_has_only_guessable_words() -> None:
    words = read_words_from_file(WORDS_PATH)
    assert words
    assert all(word.isalpha() and word.islower() for word in words)


def test_words_path_does_not_depend_on_cwd(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    assert WORDS_PATH.is_absolute()
    assert read_words_from_file(WORDS_PATH)
