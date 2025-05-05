# -*- coding: utf-8 -*-
"""
Word Probability Solver Module

Used to guess words based on the probabilities of each word in an NLTK corpus.

Copyright 2024-2025 Arun K Viswanathan
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""
from collections import Counter

import nltk

from constants import DEFAULT_NLTK_CORPUSES
from utils import print_best_guesses


class WordProbabilitySolver:
    """
    A class used to solve word puzzles based on word probabilities.

    This class uses the Natural Language Toolkit (NLTK) to analyze the frequency of words in a
    given corpus. It uses this information to guess words in Wordle.

    Attributes:
        quiet (bool): A flag indicating whether to run in quiet mode.
        br_word_freq (dict): A dictionary mapping words to their frequencies in the corpus.

    Methods:
        __init__(self, quiet, words, corpuses): Initializes the WordProbabilitySolver.
        guess(self, words): Returns the word with the highest frequency in the corpus.
    """

    def __init__(self, quiet, words, corpuses):
        """
        Initialize the object with the provided parameters.

        Parameters:
            quiet (bool): A flag indicating whether to run in quiet mode.
            words (list): A list of words to analyze.
            corpuses (list): A list of corpuses to search for words.

        Returns:
            None
        """
        self.quiet = quiet
        word_len = len(words[0])
        corpus_words = self.get_corpus_words(corpuses, word_len)
        br_word_counts = Counter(corpus_words)
        self.br_word_freq = \
            {word: br_word_counts[word] / len(corpus_words) for word in corpus_words}

    @staticmethod
    def get_corpus_words(corpuses, word_len):
        """
        Generate a list of words from the specified corpuses that have a specific length.

        :param corpuses: A list of strings representing the corpuses to extract words from.
        :param word_len: An integer representing the desired length of the words to extract.
        :return: A list of words from the corpuses that have the specified length.
        """
        if not corpuses:
            corpuses = DEFAULT_NLTK_CORPUSES
        corpus_words = []
        for corpus in corpuses:
            nltk.download(corpus)
            corpus_module = getattr(nltk.corpus, corpus)
            if corpus_module is None:
                corpus_module = nltk.corpus.brown
            corpus_words.extend([word.lower() for word in corpus_module.words()
                                 if len(word) == word_len])
        return corpus_words

    def guess(self, words):
        """
        Generate best guess for a list of words based on their scores and return the top guess.

        Parameters:
            words (list): A list of words to generate guesses for.

        Returns:
            str: The top guess word with the highest score.
        """
        word_scores = [(word, self.br_word_freq.get(word, 0)) for word in words]
        word_scores = sorted(word_scores, key=lambda item: item[1], reverse=True)
        print_best_guesses(self.quiet, word_scores)
        return word_scores[0][0]
