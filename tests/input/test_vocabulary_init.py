from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from pytest_mock.plugin import MockerFixture

from app.input import WordVocabulary


def test_init(read_words_mock: MagicMock) -> None:
    """
    Initialize the WordVocabulary instance with the given path and verify the initial state.
    """
    path = 'test_file.txt'
    instance = WordVocabulary(path)
    assert instance.words
    assert not instance.used_words
    assert len(instance.words) == 3
    read_words_mock.assert_called_once_with(path)


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
