# -*- coding: utf-8 -*-
"""
Entropy lowering solver

See https://towardsdatascience.com/information-theory-applied-to-wordle-b63b34a6538e

Copyright 2024 Arun K Viswanathan
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""
import math
from collections import Counter
from functools import reduce
from math import log
from multiprocessing import Manager, Process, cpu_count

from responses import get_response_non_interactive
from utils import chunk_list, print_best_guesses


class EntropySolver:
    """
    A class used to solve Wordle puzzles using entropy lowering.

    This class provides methods to compute entropy for a list of words and generate the best
    guess based on the computed entropy scores. The entropy is computed using the formula
    -i * log(i) for each word in the list, where i is the frequency of the word.

    Attributes
    ----------
    quiet : bool
        A flag indicating whether to run the function quietly.

    Methods
    -------
    guess(words: list) -> str:
        Generate the best guess for a list of words based on their entropy scores.

    compute_entropy(words: list) -> list:
        Compute entropy scores for each word in the given list of words.

    compute_entropy_for_word(word: str, words: list) -> tuple:
        Compute entropy for a given word.
    """

    def __init__(self, quiet, all_words):
        """
        Initialize the object with the provided parameters.

        Parameters:
            quiet (bool): A flag indicating whether to run the function quietly.
            all_words (list): A list of all possible words to be used for entropy computation.

        Returns:
            None
        """
        self.quiet = quiet
        self.all_words = all_words
        self.all_word_entropy = EntropySolver.compute_entropy(all_words, True)

    def guess(self, words):
        """
        Generate best guess for a list of words based on their entropy scores.

        Parameters:
            words (list): A list of words to generate guesses for.

        Returns:
            str: The top guess word with the lowest entropy.
        """

        if words == self.all_words:
            entropy = self.all_word_entropy
        else:
            entropy = self.compute_entropy(words, False)
        word_scores = [item for item in entropy if item[0] in words]
        word_scores = sorted(word_scores, key=lambda item: item[1], reverse=True)
        print_best_guesses(self.quiet, word_scores)
        return word_scores[0][0]

    @staticmethod
    def compute_entropy(words, parallel=False):
        """
        Compute the entropy of a list of words.

        Parameters:
            words (list): A list of words for which to compute entropy.
            parallel (bool): Flag indicating whether to compute entropy in parallel.

        Returns:
            list: A list of entropy values for each word in the input list.
        """
        if not parallel or len(words) < 800:
            entropies = []
            for word in words:
                entropies.append(EntropySolver.compute_entropy_for_word(word, words))
            return entropies
        with Manager() as manager:
            entropies = manager.list()
            chunk_size = math.ceil(len(words) / cpu_count())
            processes = []
            for chunk in chunk_list(words, chunk_size):
                process = Process(target=EntropySolver.compute_entropy_for_chunk,
                                  args=(chunk, words, entropies))
                process.start()
                processes.append(process)
            for process in processes:
                process.join()
            return list(entropies)

    @staticmethod
    def compute_entropy_for_chunk(chunk, words, entropies):
        """
        Compute entropy for a chunk of words and update the entropies list.

        :param chunk: List of words to compute entropy for
        :param words: List of all words to use for entropy calculation
        :param entropies: List to store the computed entropies
        """
        for word in chunk:
            entropies.append(EntropySolver.compute_entropy_for_word(word, words))

    @staticmethod
    def compute_entropy_for_word(word, words):
        """
        Compute the entropy for a given word compared to other words in a list.

        Parameters:
        word (str): The word for which entropy needs to be computed.
        words (list): A list of words to compare against.

        Returns:
        tuple: A tuple containing the word and its computed entropy.
        """
        responses = [get_response_non_interactive(word, other_word) for other_word in words]
        response_freq_map = Counter(responses)
        probabilities = [freq / len(words) for freq in response_freq_map.values()]
        entropy = reduce(lambda x, y: x - y * log(y), probabilities, 0)
        return word, entropy
