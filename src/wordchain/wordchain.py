# ruff: noqa: D105, D107
"""This module contains the core classes for working with WordChains."""

import string
from typing import Collection, Dict, Iterator, List, Tuple

import networkx as nx

from wordchain import errors


class WordGraph:
    """This class builds a graph of words which differ by only one letter.

    - **parameters**

        :param word_list: a list of strings all of the same length
    """

    def __init__(self, word_list: List[str]) -> None:
        if len(word_list) == 0:
            raise errors.EmptyWordListException(
                "Word list must contain at least one word"
            )
        length: int = len(word_list[0])
        for word in word_list:
            if not word.isalpha():
                raise errors.NonAlphaException(
                    f"Words in file must be alphabetical characters only. Failed on {word}"
                )

            if len(word) != length:
                raise errors.LengthMismatchException
        self.word_length: int = length
        self.word_list = set(word_list)
        self.graph: Dict[str, List[str]] = {}

    def __str__(self) -> str:
        return (
            f"Word Graph: {self.word_length} letter words. {len(self.word_list)} words."
        )

    def get_graph(self) -> Dict[str, List[str]]:
        """Get graph stored on object. Builds it if not available."""
        if not self.graph:
            self.build_word_graph()
        return self.graph

    def build_word_graph(self) -> Dict[str, List[str]]:
        """Build word graph of words which differ by one letter."""
        self.graph = {word: self.neighbours(word) for word in self.word_list}
        return self.graph

    def neighbours(self, word: str) -> List[str]:
        """Get list of words which differ by one letter from argument word."""
        nn_list = set()
        for index in range(len(word)):
            for letter in string.ascii_lowercase:
                neighbour_word = f"{word[:index]}{letter}{word[index + 1 :]}"
                if neighbour_word in self.word_list:
                    nn_list.add(neighbour_word)
        if word in nn_list:
            nn_list.remove(word)
        return list(nn_list)


class WordChainer:
    """This class takes in a word list, retrieves the word graph and provides methods for retrieving word chains.

    - **parameters**

        :param word_list: a list of strings all of the same length
    """

    def __init__(self, word_list: List[str]) -> None:
        self.word_graph: WordGraph = WordGraph(word_list)
        self.nx_graph: nx.DiGraph = nx.DiGraph(self.word_graph.get_graph())

    @property
    def word_length(self) -> int:
        """Word length. All words in a word graph have the same length."""
        return self.word_graph.word_length

    @property
    def word_list(self) -> Collection[str]:
        """All words in the word graph."""
        return self.word_graph.word_list

    @classmethod
    def from_file(cls, filename: str) -> "WordChainer":
        """Create a WordChainer object from a file containing a list of words."""
        with open(filename, encoding="utf8") as file:
            word_list = [line.strip() for line in file]
        return cls(word_list=word_list)

    def get_chains(self, start_word: str, end_word: str) -> "WordChain":
        """Given a start word and an end word, return all shortest paths between those words."""
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
    """Sequence-like object that holds the paths and other minor utilities."""

    def __init__(
        self, start_word: str, end_word: str, paths: Collection[Tuple[str, ...]]
    ) -> None:
        self.start_word = start_word
        self.end_word = end_word
        self.paths: Collection[Tuple[str, ...]] = {tuple(p) for p in paths}

    @property
    def path_count(self) -> int:
        """Number of paths of the shortest possible distance between start_word and end_word."""
        return len(self.paths)

    def __contains__(self, path: Tuple[str]) -> bool:
        return path in self.paths

    def __iter__(self) -> Iterator[Tuple[str, ...]]:
        return (p for p in self.paths)

    def __repr__(self) -> str:
        return f"WordChain({self.start_word}, {self.end_word}, {self.paths})"


class WordChainerCollection:
    """Convenience class for working with multiple word lengths."""

    def __init__(self, word_list: List[str]) -> None:
        self.original_list = list(word_list)

        self.word_lists: Dict[int, List[str]] = {}
        for word in word_list:
            self.word_lists.setdefault(len(word), []).append(word)
        self.word_chainers = {
            length: WordChainer(word_list=words)
            for length, words in self.word_lists.items()
        }

    def get_word_list(self, word_length: int) -> List[str]:
        """Get list of words of a given length."""
        return self.word_lists.get(word_length, [])

    def get_chains(self, start_word: str, end_word: str) -> WordChain:
        """Get word chain between two words of the same length."""
        try:
            return self.word_chainers[len(start_word)].get_chains(
                start_word=start_word, end_word=end_word
            )
        except KeyError:
            return WordChain(start_word=start_word, end_word=end_word, paths=set())
