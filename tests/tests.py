import pytest

from wordchain import WordChainer, WordGraph
from wordchain import errors

WORD_LIST = ["bird", "bind", "bord", "bond", "bong", "song"]

# WordChain should take list of words and build the graph
def test_word_chain():
    chainer = WordChainer(word_list=WORD_LIST)
    chains = chainer.get_chains("bird", "song")
    assert set(tuple(c) for c in chains) == {
        ("bird", "bind", "bond", "bong", "song"),
        ("bird", "bord", "bond", "bong", "song"),
    }


def test_word_chain_fails_when_words_have_different_lengths():
    word_list = ["hello", "love"]

    with pytest.raises(errors.LengthMismatchException):
        WordChainer(word_list=word_list)


def test_word_neighbours():
    wg = WordGraph(WORD_LIST)
    neighbours = wg.neighbours("bird")
    assert set(neighbours) == {"bind", "bord"}
    neighbours = wg.neighbours("bond")
    assert set(neighbours) == {"bind", "bord", "bong"}
