from __future__ import annotations

from pytest_mock.plugin import MockerFixture

from hangman.input import WordVocabulary


def test_returns_word_from_list(mocker: MockerFixture) -> None:
    """
    Test the function that returns a word from a list, using mocker to patch dependencies.
    """
    mocker.patch(
        "hangman.input.read_words_from_file",
        return_value=["apple", "banana", "orange"],
    )
    mocker.patch('hangman.input.WordVocabulary.random_idx', return_value=0)
    expected = 'apple'
    instance = WordVocabulary('test_file.txt')
    result = instance.random_word()
    assert result == expected
