import pytest

from wordchain.wordchain import WordChainer, WordGraph, WordChainerCollection
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


def test_str_repr():
    """Case with no neighbours should be handled gracefully"""
    word_graph = WordGraph(WORD_LIST)
    assert "Word Graph: 4 letter words. 6 words." == str(word_graph)


def test_word_chain():
    """WordChain should take list of words and build the graph"""
    chainer = WordChainer(word_list=WORD_LIST)
    chains = chainer.get_chains("bird", "song")
    assert chains.paths == {
        ("bird", "bind", "bond", "bong", "song"),
        ("bird", "bord", "bond", "bong", "song"),
    }
    assert chains.path_count == 2
    for path in chains:
        assert len(path) == 5


def test_no_word_chain():
    """WordChain should take list of words and build the graph. Get empty list if no chain exists"""
    chainer = WordChainer(word_list=WORD_LIST)
    chains = chainer.get_chains("bird", "abcd")
    assert chains.paths == set()


def test_mismatch_word_chain():
    """WordChain should take list of words and build the graph. Get empty list if no chain exists"""
    chainer = WordChainer(word_list=WORD_LIST)
    with pytest.raises(errors.LengthMismatchException):
        chainer.get_chains("birds", "song")


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


MIXED_WORD_LIST = ["man", "apt", "oat", "mat", "ape", "opt"] + WORD_LIST


def test_word_chain_collection():
    wcc = WordChainerCollection(word_list=MIXED_WORD_LIST)
    assert set(wcc.word_lists.keys()) == {3, 4}
    assert set(wcc.word_chainers.keys()) == {3, 4}

    assert ("ape", "apt", "opt", "oat", "mat", "man") in wcc.get_chains("ape", "man")
    assert ("bird", "bind", "bond", "bong", "song") in wcc.get_chains("bird", "song")
    assert len(wcc.get_chains("bride", "groom").paths) == 0
