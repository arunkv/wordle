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

Copyright 2024-2025 Arun K Viswanathan
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""

import logging

import nltk


def get_word_list(word_lists: list) -> set:
    """
    Generates a set of words from a list of word files.

    Args:
        word_lists (list): A list of file paths to word files.

    Returns:
        set: A set of words from the word files or the NLTK corpus words.
    """
    word_list = set()
    for word_file in word_lists:
        try:
            with open(word_file, 'r', encoding='utf-8') as file:
                word_list = word_list.union([line.strip() for line in file])
        except FileNotFoundError:
            print(f"File {word_file} not found.")
    if len(word_list) > 0:
        return word_list
    try:
        nltk_words = nltk.corpus.words.words()
    except LookupError:
        nltk.download('words')
        logging.info("Downloading NLTK corpus")
        nltk_words = nltk.corpus.words.words()
        logging.info("NLTK corpus downloaded with %s words", len(nltk_words))
    return nltk_words
