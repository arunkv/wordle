# -*- coding: utf-8 -*-
"""
Word List Management Module

This module provides functionality for managing the word list used in the Wordle solver game.
It includes a function `get_word_list` that retrieves the word list from a specified file or
from the NLTK corpus if the file does not exist.

The `get_word_list` function first checks if the specified file exists and is a file. If it is,
it reads the file and returns a list of words. If the file does not exist, it attempts to
retrieve the word list from the NLTK corpus. If the NLTK corpus is not available, it downloads
the corpus and then retrieves the word list.

This module is part of a Wordle solver game and is used to provide the list of words that the
game can use.

Copyright 2024 Arun K Viswanathan
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""

import logging
import os

import nltk


def get_word_list(word_list):
    """
    Retrieves the word list from specified file or NLTK words corpus if the file does not exist.

    This function first checks if the specified file exists and is a file. If it is, it reads the
    file and returns a list of words. If the file does not exist, it attempts to retrieve the word
    list from the NLTK words corpus. If the NLTK words corpus is not available, it downloads the
    corpus and then retrieves the word list.

    Parameters:
    word_list (str): The path to the file containing the word list.

    Returns:
    list: A list of words from the specified file or the NLTK corpus.
    """

    try:
        if os.path.isfile(word_list):
            logging.info("Using custom dictionary: %s", word_list)
            with open(word_list, 'r', encoding='utf-8') as word_file:
                return [line.strip() for line in word_file]
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        try:
            nltk_words = nltk.corpus.words.words()
        except LookupError:
            nltk.download('words')
            logging.info("Downloading NLTK corpus")
            nltk_words = nltk.corpus.words.words()
            logging.info("NLTK corpus downloaded with %s words", len(nltk_words))
        return nltk_words
