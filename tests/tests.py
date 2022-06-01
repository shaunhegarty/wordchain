from wordchain import WordChainer, WordGraph

WORD_LIST = ['bird', 'bind', 'bord', 'bond', 'bong', 'song']

# WordChain should take list of words and build the graph
def test_word_chain():
    chainer = WordChainer(word_list=WORD_LIST)
    chains = chainer.get_chains('bird', 'song')
    assert set(tuple(c) for c in chains) ==  {('bird', 'bind', 'bond', 'bong', 'song'), ('bird', 'bord', 'bond', 'bong', 'song')}


def test_word_neighbours():
    wg = WordGraph(WORD_LIST)
    neighbours = wg.neighbours('bird')
    assert set(neighbours) == {'bind', 'bord'}
