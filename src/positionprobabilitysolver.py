# -*- coding: utf-8 -*-
"""
Probabilistic Solver Module

This module contains the ProbabilisticSolver class which is used to guess words based on the
probabilities of each letter at each position in a given list of words. The class computes
the letter probabilities for a list of words and uses these probabilities to score and guess
the words.

The ProbabilisticSolver class includes methods to compute letter probabilities, compute word
scores based on these probabilities, and guess words based on their scores.

This module is part of a Wordle solver game and is used to make educated guesses based on
the letter probabilities in the given word list.

Copyright 2024 Arun K Viswanathan
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""
from collections import Counter

from utils import print_best_guesses


class PositionProbabilitySolver:
    """
    A class used to guess words based on the probabilities of each letter at each position in a
    given list of words.

    ...

    Attributes
    ----------
    letter_probabilities : list
        A list of dictionaries, where each dictionary maps a letter to its probability at the
        corresponding position in the words.

    Methods
    -------
    guess(words):
        Returns the word with the highest score from the given list of words.
    compute_letter_probabilities(words):
        Computes probability of each letter appearing at each position in the given list of words.
    compute_word_scores(words):
        Computes the score for each word in the given list of words based on the probabilities of
        each letter at each position.
    compute_word_score(word):
        Computes score for a given word based on the probabilities of each letter at each position.
    """

    def __init__(self, quiet, words):
        self.quiet = quiet
        self.letter_probabilities = PositionProbabilitySolver.compute_letter_probabilities(words)

    def guess(self, words):
        """
        Returns the word with the highest score from the given list of words.

        This function calculates the score of each word by calling the `compute_word_scores`
        function for the list of words. It then returns the word with the highest score.

        Args:
            words (list): The list of words to compute scores for and guess from.

        Returns:
            str: The word with the highest score.
        """
        word_scores = self.compute_word_scores(words)
        print_best_guesses(self.quiet, word_scores)
        return word_scores[0][0]  # Pick the top probability word

    @staticmethod
    def compute_letter_probabilities(words):
        """
        Computes the probability of each letter appearing at each position in the given list of
        words.

        This function calculates the frequency of each letter at each position in the words, and
        then divides each frequency by the total number of words to get the probability.

        Args:
            words (list): The list of words to compute letter probabilities for.

        Returns:
            list: A list of dictionaries, where each dictionary maps a letter to its probability at
             the corresponding position in the words.
        """
        letter_frequencies = [Counter(word[i] for word in words)
                              for i in range(len(words[0]))]
        letter_probabilities = [{letter: freq / len(words) for letter, freq in frequencies.items()}
                                for frequencies in letter_frequencies]
        return letter_probabilities

    def compute_word_scores(self, words):
        """
        Computes the score for each word in the given list of words based on the probabilities of
        each letter at each position.

        This function calculates the score of each word by calling the `compute_word_score` function
        for each word in the list. The scores are then sorted in descending order.

        Args:
            words (list): The list of words to compute scores for.

        Returns:
            list: A list of tuples, where each tuple contains a word and its score, sorted in
                  descending order of the scores.
        """
        word_scores = [(word, self.compute_word_score(word)) for word in words]
        word_scores.sort(key=lambda x: x[1], reverse=True)
        return word_scores

    def compute_word_score(self, word):
        """
        Computes score for a given word based on the probabilities of each letter at each position.

        Args:
            word (str): The word to compute the score for.

        Returns:
            float: The score of the word.
        """
        return sum(self.letter_probabilities[i].get(letter, 0.0) for i, letter in enumerate(word))
