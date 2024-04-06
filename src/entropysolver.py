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

from responses import get_response_non_interactive
from utils import quiet_print


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
        self.response_scores = self.compute_response_scores(words)

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
        if not self.quiet:
            quiet_print(self.quiet, "Best guesses: ")
            for _, (word, score) in enumerate(word_scores[:5]):
                quiet_print(self.quiet, f"\t- {word}: ({score:.2f})")
        return word_scores[0][0]

    @staticmethod
    def compute_response_scores(words):
        """
        For each word in words, compare to all other words using the get_response_non_interactive
        function and compute the percentage of words that are resulting in an 'xxxxx' response.

        Parameters:
            words (list): A list of words to compare.

        Returns:
            dict: A dictionary with each word as the key and the percentage of 'xxxxx' responses
            as the value.
        """
        response_scores = []
        for word in words:
            response_freq_map = defaultdict(int)
            for other_word in words:
                if word != other_word:
                    response = get_response_non_interactive(word, other_word)
                    response_freq_map[response] += 1

            cumulative_response_score = 0
            for response, freq in response_freq_map.items():
                response_score = EntropySolver.compute_response_score(response)
                cumulative_response_score += response_score * freq

            response_scores.append((word, cumulative_response_score / len(words)))
        return response_scores

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
            if char == '=':
                score += 1
            elif char == 'o':
                score += 0.3
        return score
