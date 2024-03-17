from __future__ import annotations

import pytest
from pytest_mock.plugin import MockerFixture

from app.input import WordVocabulary


@pytest.fixture
def read_words_mock(mocker: MockerFixture) -> None:
    _read_words_mock = mocker.patch('app.input.read_words_from_file', return_value=['word1', 'word2', 'word3'])
    return _read_words_mock


def test_random_idx_within_range(read_words_mock) -> None:
    """
    Generate a random index within the range of the number of words in the WordVocabulary instance.
    """
    instance = WordVocabulary('test_file.txt')
    idx = instance.random_idx()
    assert 0 <= idx < len(instance.words)


def test_random_idx_not_used_before(read_words_mock) -> None:
    """
    Function to test the random_idx method of WordVocabulary class when the index is not used before.
    """
    instance = WordVocabulary('test_file.txt')
    instance.used_words = [0, 2]
    used_words_before = instance.used_words.copy()
    _ = instance.random_idx()
    new_used_words = instance.used_words
    assert used_words_before == new_used_words[:-1]


def test_random_idx_not_used_before_test2(read_words_mock) -> None:
    """
    Function to test the random_idx method when the index has not been used before in the WordVocabulary class.
    Uses a mock for reading words. Verifies that the random index is selected correctly and that the list of used words is updated accordingly.
    """
    instance = WordVocabulary('test_file.txt')
    instance.used_words = [0, 2]
    expected_used_words = [0, 2, 1]
    expected_idx = 1
    idx = instance.random_idx()
    assert idx == expected_idx
    assert expected_used_words == instance.used_words
