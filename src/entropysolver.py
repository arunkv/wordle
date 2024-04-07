# -*- coding: utf-8 -*-
"""
Entropy lowering solver

See https://towardsdatascience.com/information-theory-applied-to-wordle-b63b34a6538e

Copyright 2024 Arun K Viswanathan
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""
from collections import defaultdict
from multiprocessing import Pool, cpu_count

from constants import EXACT_MATCH, PARTIAL_MATCH
from responses import get_response_non_interactive
from utils import print_best_guesses


class EntropySolver:
    """
    EntropySolver is a class that provides methods to solve the Wordle game by lowering entropy.

    Attributes:
        quiet (bool): A flag indicating whether to run the function quietly.
        response_scores (list): A list of tuples, each containing a word and its corresponding
         bad response percentage.

    Methods:
        __init__(self, quiet, words): Initializes the EntropySolver object with the provided
        parameters.
        guess(self, words): Generates the best guess for a list of words based on their entropy
        scores.
        compute_bad_response_percentages(words): Computes the percentage of bad responses for each
        word in the provided list.
    """

    def __init__(self, quiet, words):
        """
        Initialize the object with the provided parameters.

        Parameters:
            quiet (bool): A flag indicating whether to run the function quietly.
            words (list): A list of words to compute bad response percentages.

        Returns:
            None
        """
        self.quiet = quiet
        self.all_words = words
        self.response_scores = self.compute_response_scores()

    def guess(self, words):
        """
        Generate best guess for a list of words based on their entropy scores.

        Parameters:
            words (list): A list of words to generate guesses for.

        Returns:
            str: The top guess word with the lowest entropy.
        """
        word_scores = [item for item in self.response_scores if item[0] in words]
        word_scores = sorted(word_scores, key=lambda item: item[1], reverse=True)
        print_best_guesses(self.quiet, word_scores)
        return word_scores[0][0]

    def compute_response_scores(self):
        """
        Compute response scores using multiprocessing for each word in the given list of words.
        """
        with Pool(cpu_count()) as pool:
            response_scores = pool.map(self.compute_response_score_for_word, self.all_words)
        return response_scores

    def compute_response_score_for_word(self, word):
        """
        Compute response score for a given word.

        Parameters:
            word (str): The word for which the response score is being computed.

        Returns:
            tuple: A tuple containing the word and the computed cumulative response score.
        """
        response_freq_map = defaultdict(int)
        for other_word in self.all_words:
            if word != other_word:
                response = get_response_non_interactive(word, other_word)
                response_freq_map[response] += 1

        cumulative_response_score = 0
        for response, freq in response_freq_map.items():
            response_score = EntropySolver.compute_response_score(response)
            cumulative_response_score += response_score * freq

        return word, cumulative_response_score / len(self.all_words)

    @staticmethod
    def compute_response_score(response):
        """
        Compute the score of a given response based on the occurrences of '=' and 'o' characters.

        Parameters:
            response (str): The response string to calculate the score from.

        Returns:
            float: The calculated score based on the response string.
        """
        score = 0
        for char in response:
            if char == EXACT_MATCH:
                score += 1
            elif char == PARTIAL_MATCH:
                score += 0.1
        return score
