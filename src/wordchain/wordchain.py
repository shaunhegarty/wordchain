import string
import networkx as nx


class WordGraph:

    def __init__(self, word_list):
        self.word_list = set(word_list)
        self.graph = {}

    def get_graph(self):
        if not self.graph:
            self.build_word_graph()
        return self.graph

    def build_word_graph(self):
        self.graph = {word: self.neighbours(word) for word in self.word_list}
        return self.graph
    
    def neighbours(self, word):
        nn_list = set()
        for index in range(len(word)):
            for letter in string.ascii_lowercase:
                neighbour_word = f'{word[:index]}{letter}{word[index + 1:]}'
                if neighbour_word in self.word_list:
                    nn_list.add(neighbour_word)
        nn_list.remove(word)
        return list(nn_list)


class WordChainer:
    
    def __init__(self, word_list):
        self.word_list = word_list
        self.word_graph = WordGraph(word_list)
        self.nx_graph = nx.DiGraph(self.word_graph.get_graph())
    
    def get_chains(self, start_word, end_word):
        return [p for p in nx.all_shortest_paths(self.nx_graph, start_word, end_word)]



