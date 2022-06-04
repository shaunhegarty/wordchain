""" This module contains the core classes for working with WordChains"""

import string

from typing import Set, Tuple, List, Generator

import networkx as nx

from wordchain import errors


class WordGraph:
    """This class builds a graph of words which differ by only one letter.

    - **parameters**

        :param word_list: a list of strings all of the same length"""

    def __init__(self, word_list: List[str]):

        length = None
        for word in word_list:
            if not word.isalpha():
                raise errors.NonAlphaException(
                    f"Words in file must be alpabetical characters only. Failed on {word}"
                )

            if not length:
                length = len(word)
            elif len(word) != length:
                raise errors.LengthMismatchException

        self.word_list = set(word_list)
        self.graph = {}

    def get_graph(self) -> Set[List[str]]:
        """Get graph stored on object. Builds it if not available."""
        if not self.graph:
            self.build_word_graph()
        return self.graph

    def build_word_graph(self) -> Set[List[str]]:
        """Build word graph of words which differ by one letter"""
        self.graph = {word: self.neighbours(word) for word in self.word_list}
        return self.graph

    def neighbours(self, word: str) -> List[str]:
        """Get list of words which differ by one letter from argument word"""
        nn_list = set()
        for index in range(len(word)):
            for letter in string.ascii_lowercase:
                neighbour_word = f"{word[:index]}{letter}{word[index + 1:]}"
                if neighbour_word in self.word_list:
                    nn_list.add(neighbour_word)
        if word in nn_list:
            nn_list.remove(word)
        return list(nn_list)


class WordChainer:
    """This class takes in a word list, retrieves the word graph and provides methods for
    retrieving word chains

    - **parameters**

        :param word_list: a list of strings all of the same length"""

    def __init__(self, word_list):
        self.word_list = word_list
        self.word_graph = WordGraph(word_list)
        self.nx_graph = nx.DiGraph(self.word_graph.get_graph())

    @classmethod
    def from_file(cls, filename):
        with open(filename, encoding='utf8') as file:
            word_list = [line.strip() for line in file]
        return cls(word_list=word_list)

    def get_chains(self, start_word: str, end_word: str) -> Set[Tuple[str]]:
        """Given a start word and an end word, return all shortest paths between those words"""
        paths =  {
            tuple(p) for p in nx.all_shortest_paths(self.nx_graph, start_word, end_word)
        }
        return WordChain(start_word=start_word, end_word=end_word, paths=paths)


class WordChain:
    """ Sequence-like object that holds the paths and other minor utilities"""
    def __init__(self, start_word: str, end_word: str, paths: Set[Tuple[str]]):
        self.start_word = start_word
        self.end_word = end_word
        self.paths = {tuple(p) for p in paths}

    @property
    def path_count(self) -> int:
        """ Number of paths of the shortest possible distance between start_word and end_word"""
        return len(self.paths)

    def __contains__(self, path: Tuple[str]) -> bool:
        return path in self.paths

    def __iter__(self) -> Generator:
        return (p for p in self.paths)
