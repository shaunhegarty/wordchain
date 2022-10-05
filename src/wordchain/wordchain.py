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
                    f"Words in file must be alphabetical characters only. Failed on {word}"
                )

            if not length:
                length = len(word)
            elif len(word) != length:
                raise errors.LengthMismatchException
        self.word_length = length
        self.word_list = set(word_list)
        self.graph = {}

    def __str__(self):
        return (
            f"Word Graph: {self.word_length} letter words. {len(self.word_list)} words."
        )

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

    def __init__(self, word_list: str):
        self.word_graph = WordGraph(word_list)
        self.nx_graph = nx.DiGraph(self.word_graph.get_graph())

    @property
    def word_length(self) -> int:
        return self.word_graph.word_length

    @property
    def word_list(self) -> List[str]:
        return self.word_graph.word_list

    @classmethod
    def from_file(cls, filename: str):
        with open(filename, encoding="utf8") as file:
            word_list = [line.strip() for line in file]
        return cls(word_list=word_list)

    def get_chains(self, start_word: str, end_word: str) -> Set[Tuple[str]]:
        """Given a start word and an end word, return all shortest paths between those words"""
        if len(start_word) != len(end_word):
            raise errors.LengthMismatchException(
                f"Can't find path between two words of a different length: {start_word} {end_word}"
            )

        try:
            paths = {
                tuple(p)
                for p in nx.all_shortest_paths(self.nx_graph, start_word, end_word)
            }
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            paths = set()
        return WordChain(start_word=start_word, end_word=end_word, paths=paths)


class WordChain:
    """Sequence-like object that holds the paths and other minor utilities"""

    def __init__(self, start_word: str, end_word: str, paths: Set[Tuple[str]]):
        self.start_word = start_word
        self.end_word = end_word
        self.paths = {tuple(p) for p in paths}

    @classmethod
    def empty(cls):
        return cls(None, None, set())

    @property
    def path_count(self) -> int:
        """Number of paths of the shortest possible distance between start_word and end_word"""
        return len(self.paths)

    def __contains__(self, path: Tuple[str]) -> bool:
        return path in self.paths

    def __iter__(self) -> Generator:
        return (p for p in self.paths)

    def __repr__(self) -> str:
        return f'WordChain({self.start_word}, {self.end_word}, {self.paths})'


class WordChainerCollection:
    def __init__(self, word_list):
        self.original_list = list(word_list)

        self.word_lists = {}
        for word in word_list:
            self.word_lists.setdefault(len(word), []).append(word)
        self.word_chainers = {
            length: WordChainer(word_list=words)
            for length, words in self.word_lists.items()
        }

    def get_word_list(self, word_length):
        return self.word_lists.get(word_length, [])

    def get_chains(self, start_word: str, end_word: str) -> Set[Tuple[str]]:
        try:
            return self.word_chainers[len(start_word)].get_chains(
                start_word=start_word, end_word=end_word
            )
        except KeyError:
            return WordChain(start_word=start_word, end_word=end_word, paths=set())
