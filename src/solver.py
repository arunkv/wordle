# -*- coding: utf-8 -*-
"""
Wordle Solver Algorithm

This module contains the algorithm for solving Wordle. It includes functions for trimming the word
list by the provided search space, computing letter probabilities for each position in the word,
computing the score for a word given the individual letter probabilities, processing user responses,
and the main solve function which uses all these helper functions to solve the Wordle game.

The `solve` function is the main entry point. It takes command-line arguments, loads the word list,
and starts the game loop. In each iteration of the loop, it makes a guess, processes the user's
response, and updates the search space and known letters accordingly. The loop continues until the
Wordle is solved or the maximum number of tries is reached.

This module is meant to be imported and used by the `wordle.py` script. It does not provide any
command-line interface of its own.

Copyright 2024 Arun K Viswanathan
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""

import logging
import string
from collections import Counter

# from constants import NLTK_CORPUSES
from constants import NLTK_CORPUSES
from positionprobabilitysolver import PositionProbabilitySolver
from entropysolver import EntropySolver
from responses import display_response, get_response, process_response
from wordprobabilitysolver import WordProbabilitySolver
from stats import finalize_stats, load_stats, save_stats
from utils import quiet_print
from wordlist import get_word_list


def trim_word_list_by_search_space(word_list, search_space, known_letters):
    """
    Trims the word list by the provided search space and known letters.

    This function filters the word list by ensuring that each word only contains letters that are
    in the corresponding position's search space and that all known letters are in the word.

    Args:
        word_list (list): The list of words to trim.
        search_space (list): A list of sets, where each set contains the possible letters for the
                             corresponding position in the word.
        known_letters (list): A set of letters that are known to be in the word.

    Returns:
        list: The trimmed word list.
    """
    return [word for word in word_list
            if all(word[i] in letters for i, letters in enumerate(search_space))
            and are_known_letters_in_word(word, known_letters)]


def are_known_letters_in_word(word, known_letters):
    """
    Checks if all letters in the `known_letters` list, including duplicates, are present in a word.

    This function uses a Counter object from the `collections` module in Python to count the
    occurrences of each letter in the word and in the `known_letters` list. It then checks if for
    every letter in `known_letters`, the count in the word is greater than or equal to the count
    in `known_letters`.

    Args:
        word (str): The word in which to check for the presence of the known letters.
        known_letters (list): A list of known letters to check for in the word.

    Returns:
        bool: True if all letters in `known_letters` (including duplicates) are present in `word`,
              False otherwise.
    """
    word_counter = Counter(word)
    known_letters_counter = Counter(known_letters)
    return all(word_counter[letter] >= count for letter, count in known_letters_counter.items())


def solve(args):
    """
    The main function for the Wordle solver.

    This function takes command-line arguments, loads the word list, and starts the game loop. In
    each iteration of the loop, it makes a guess, processes the user's response, and updates the
    search space and known letters accordingly. The loop continues until the Wordle is solved or
    the maximum number of tries is reached.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.

    Returns:
        None
    """
    all_words = sorted([word for word in get_word_list(args.dict)
                        if len(word) == args.len and not word[0].isupper()])
    logging.info("Word list loaded with %s words", len(all_words))
    if args.solver == 'position':
        solver = PositionProbabilitySolver(args.quiet, all_words)
    elif args.solver == 'word':
        solver = WordProbabilitySolver(args.quiet, all_words, NLTK_CORPUSES)
    elif args.solver == 'entropy':
        solver = EntropySolver(args.quiet, all_words)
    else:
        solver = PositionProbabilitySolver(args.quiet, all_words)
    stats = load_stats()
    if args.continuous:
        if args.non_interactive:
            for word in all_words:
                solver_worker(all_words, word, args, solver, stats)
                quiet_print(args.quiet)
        else:
            while True:
                solver_worker(all_words, None, args, solver, stats)
                quiet_print(args.quiet)
    else:
        solver_worker(all_words, args.word, args, solver, stats)
    save_stats(stats)


def solver_worker(all_words, word, args, solver, stats):
    """
    A function that serves as a solver worker, iterating through a list of words and processing
    responses until a solution is found or the maximum number of tries is reached.
    Parameters:
    - all_words: a list of all words
    - word: the word to solve in non-interactive mode
    - args: a dictionary of arguments
    - solver: the solver object
    - stats: a dictionary containing statistics
    Returns:
    - None
    """
    stats['played'] = stats.get('played', 0) + 1
    search_space = [set(string.ascii_lowercase) for _ in range(args.len)]
    known_letters = []
    solution = None
    tries = 0
    words = all_words.copy()
    while tries < args.tries:
        if len(words) == 0:
            quiet_print(args.quiet, "No words left in the dictionary!")
            break

        quiet_print(args.quiet, f"Round: {(tries + 1)}")
        quiet_print(args.quiet, f"Current possible answers: {len(words)}")

        # Generate a guess
        guess = solver.guess(words)
        words.remove(guess)
        quiet_print(args.quiet, f"Guess: {guess}")
        tries += 1

        # Get the response
        response = get_response(args.non_interactive, word, guess, args.len)
        display_response(args.quiet, response)

        # Process the response
        if response == 'q':  # Exit
            quiet_print(args.quiet, "Aborting!")
            break
        if response == 'i':  # Try another word since Wordle didn't accept this word
            tries -= 1
            continue
        if response == '=' * args.len:  # Wordle solved
            quiet_print(args.quiet, f"Wordle solved in {tries} tries")
            solution = guess
            break
        process_response(guess, response, search_space, known_letters, args.len)

        # Trim the word list based on the search space and known letters
        logging.debug("Known letters: %s", known_letters)
        logging.debug("Search space: %s", search_space)
        words = trim_word_list_by_search_space(words, search_space, known_letters)
        logging.info("Words left: %s", len(words))
        logging.debug("Words: %s", words)
        quiet_print(args.quiet, "")  # New line for better readability
    finalize_stats(word, args, stats, solution, tries)
