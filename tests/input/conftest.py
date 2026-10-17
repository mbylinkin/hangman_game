from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from pytest_mock.plugin import MockerFixture


@pytest.fixture
def read_words_mock(mocker: MockerFixture) -> MagicMock:
    """
    Fixture for mocking the read_words_from_file function to return a list of words.
    """
    return mocker.patch('hangman.input.read_words_from_file', return_value=['word1', 'word2', 'word3'])
