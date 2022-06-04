import pytest

from wordchain import WordChainer, WordGraph
from wordchain import errors

WORD_LIST = ["bird", "bind", "bord", "bond", "bong", "song"]


def test_word_neighbours():
    """Neighbours should consist of all words which differ by one letter"""
    word_graph = WordGraph(WORD_LIST)
    neighbours = word_graph.neighbours("bird")
    assert set(neighbours) == {"bind", "bord"}
    neighbours = word_graph.neighbours("bond")
    assert set(neighbours) == {"bind", "bord", "bong"}


def test_word_no_neighbours():
    """Case with no neighbours should be handled gracefully"""
    word_graph = WordGraph(WORD_LIST)
    neighbours = word_graph.neighbours("zeta")
    assert len(neighbours) == 0


def test_word_chain():
    """WordChain should take list of words and build the graph"""
    chainer = WordChainer(word_list=WORD_LIST)
    chains = chainer.get_chains("bird", "song")
    assert chains.paths == {
        ("bird", "bind", "bond", "bong", "song"),
        ("bird", "bord", "bond", "bong", "song"),
    }


def test_word_chain_fails_when_words_have_different_lengths():
    """WordChain should raise an exception when words of different lengths are provided"""
    word_list = ["hello", "goodbye"]

    with pytest.raises(errors.LengthMismatchException):
        WordChainer(word_list=word_list)


def test_word_chain_from_file():
    """WordChain should take list of words from file and build the graph and chains"""
    chainer = WordChainer.from_file("tests/files/simple-word-list.txt")
    chains = chainer.get_chains("ape", "man")
    assert ("ape", "apt", "opt", "oat", "mat", "man") in chains


def test_rubbish_chain_from_file():
    """WordChain should raise exception due to getting rubbish"""
    with pytest.raises(errors.NonAlphaException):
        WordChainer.from_file("tests/files/rubbish.txt")
