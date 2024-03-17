from __future__ import annotations

import pytest
from pytest_mock.plugin import MockerFixture

from app.input import WordVocabulary


@pytest.fixture
def read_words_mock(mocker: MockerFixture):
    """
    Fixture for mocking the read_words_from_file function to return a list of words.
    """
    _read_words_mock = mocker.patch('app.input.read_words_from_file', return_value=['word1', 'word2', 'word3'])
    return _read_words_mock


def test_init(read_words_mock) -> None:
    """
    Initialize the WordVocabulary instance with the given path and verify the initial state.
    """
    path = 'test_file.txt'
    instance = WordVocabulary(path)
    assert instance.words
    assert not instance.used_words
    assert len(instance.words) == 3


def test_init_file_not_found() -> None:
    """
    Test function for initializing when file is not found.
    """
    with pytest.raises(FileNotFoundError):
        WordVocabulary('nonexistent_file.txt')


def test_init_empty_file(mocker: MockerFixture) -> None:
    """
    Test function for initializing an empty file.
    """
    mocker.patch('app.input.read_words_from_file', return_value=[])
    instance = WordVocabulary('empty_file.txt')
    assert len(instance.used_words) == 0
