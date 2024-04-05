# -*- coding: utf-8 -*-
"""
Entropy lowering solver

See https://towardsdatascience.com/information-theory-applied-to-wordle-b63b34a6538e

Copyright 2024 Arun K Viswanathan
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""

from responses import get_response_non_interactive


class EntropySolver:
    """
    EntropySolver is a class that provides methods to solve the Wordle game by lowering entropy.

    Attributes:
        quiet (bool): A flag indicating whether to run the function quietly.
        bad_response_percent (list): A list of tuples, each containing a word and its corresponding
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
        self.bad_response_percent = self.compute_bad_response_percentages(words)

    def guess(self, words):
        """
        Generate best guess for a list of words based on their entropy scores.

        Parameters:
            words (list): A list of words to generate guesses for.

        Returns:
            str: The top guess word with the lowest entropy.
        """
        word_scores = [item for item in self.bad_response_percent if item[0] in words]
        word_scores = sorted(word_scores, key=lambda item: item[1])
        return word_scores[0][0]

    @staticmethod
    def compute_bad_response_percentages(words):
        """
        For each word in words, compare to all other words using the get_response_non_interactive
        function and compute the percentage of words that are resulting in an 'xxxxx' response.

        Parameters:
            words (list): A list of words to compare.

        Returns:
            dict: A dictionary with each word as the key and the percentage of 'xxxxx' responses
            as the value.
        """
        response_percentages = []
        for word in words:
            counter = 0
            for other_word in words:
                if word != other_word:
                    response = get_response_non_interactive(word, other_word)
                    if response.count('x') > 0:
                        counter += 1
            response_percentages.append((word, (counter / len(words)) * 100))
        response_percentages = sorted(response_percentages, key=lambda item: item[1])
        return response_percentages
