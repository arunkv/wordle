# -*- coding: utf-8 -*-
"""
Word Probability Solver Module

Copyright 2024 Arun K Viswanathan
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""
import ssl
from collections import Counter

import nltk


class WordProbabilitySolver:
    def __init__(self, quiet, words, corpus='brown'):
        self.quiet = quiet
        word_len = len(words[0])
        nltk.download(corpus)
        corpus_module = getattr(nltk.corpus, corpus)
        if corpus_module is None:
            corpus_module = nltk.corpus.brown
        corpus_words = [word.lower() for word in corpus_module.words() if len(word) == word_len]
        br_word_counts = Counter(corpus_words)
        self.br_word_freq = {word: br_word_counts[word] / len(corpus_words) for word in
                             corpus_words}

    def guess(self, words):
        word_frequencies = [(word, self.br_word_freq.get(word, 0)) for word in words]
        return max(word_frequencies, key=lambda x: x[1])[0]
