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

from constants import RESPONSE_PROMPT
from probabilisticsolver import ProbabilisticSolver
from stats import load_stats, save_stats
from utils import quiet_print
from wordlist import get_word_list


def get_response(length):
    """
    Prompts the user for a response and validates it.

    This function repeatedly prompts the user for a response until a valid response is given. A
    valid response is either 'q', 'i', or a string of 'x', 'o', and '=' characters of the same
    length as the provided `length` argument.

    Args:
        length (int): The expected length of the response.

    Returns:
        str: The user's response.
    """
    while True:
        response = input(RESPONSE_PROMPT)
        response = response.strip().lower()
        logging.info("Response: %s", response)
        if (all(char in {'x', 'o', '='} for char in response) and len(response) == length
                or response == 'i' or response == 'q'):
            break
        print("Invalid response. Please try again.")
    return response


def get_response_non_interactive(word, guess):
    """
    Returns the response for a given word and guess.

    This function calculates the response for a given word and guess by comparing the letters at
    each position in the word and guess. It returns a string of 'x', 'o', and '=' characters
    indicating the matches between the word and guess.

    Args:
        word (str): The word to compare against.
        guess (str): The guess to compare with the word.

    Returns:
        str: The response string.
    """
    response = ''
    for word_letter, guess_letter in zip(word, guess):
        if word_letter == guess_letter:
            response += '='
        elif guess_letter in word:
            num_occurrences = Counter(word)[guess_letter]
            num_exact_matches = sum(1 for w, g in zip(word, guess)
                                    if w == guess_letter and g == guess_letter)
            if num_exact_matches == 0 or num_occurrences < num_exact_matches:
                response += 'o'
            else:
                response += 'x'
        else:
            response += 'x'
    return response


def process_response(guess, response, search_space, known_letters, length):
    """
    Processes the user's response to a guess.

    This function updates the search space and known letters based on the user's response. It
    processes '=' responses first, then 'o' responses, and finally 'x' responses. For each type of
    response, it updates the known letters and the search space accordingly.

    Args:
        guess (str): The guess that was made.
        response (str): The user's response to the guess.
        search_space (list): A list of sets, where each set contains the possible letters for the
                             corresponding position in the word.
        known_letters (list): A set of letters that are known to be in the word.
        length (int): The length of the word.

    Returns:
        None
    """
    known_letters.clear()
    # Process '=' responses first
    for i, response_letter in enumerate(response):
        if response_letter == '=':
            known_letters.append(guess[i])
            search_space[i] = {guess[i]}

    # Then process 'o' responses
    for i, response_letter in enumerate(response):
        if response_letter == 'o':
            known_letters.append(guess[i])
            search_space[i].discard(guess[i])

    # Finally, process 'x' responses
    for i, response_letter in enumerate(response):
        if response_letter == 'x':
            search_space[i].discard(guess[i])
            other_exact_match_positions = set()
            other_partial_match_positions = set()
            for j, _ in enumerate(search_space):
                if j != i and guess[j] == guess[i]:
                    if response[j] == 'o':
                        other_partial_match_positions.add(j)
                    elif response[j] == '=':
                        other_exact_match_positions.add(j)
            if not other_partial_match_positions:
                for j in set(range(length)) - {i} - other_exact_match_positions:
                    search_space[j].discard(guess[i])


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
    words = [word for word in get_word_list(args.dict)
             if len(word) == args.len and not word[0].isupper()]
    logging.info("Word list loaded with %s words", len(words))

    solver = ProbabilisticSolver(args.quiet, words)
    search_space = [set(string.ascii_lowercase) for _ in range(args.len)]
    known_letters = []
    solution = None

    stats = load_stats()
    stats['played'] = stats.get('played', 0) + 1
    save_stats(stats)

    tries = 0
    while tries < args.tries:
        if len(words) == 0:
            quiet_print(args.quiet, "No words left in the dictionary!")
            break

        quiet_print(args.quiet, f"Round: {(tries + 1)}")
        quiet_print(args.quiet, f"Current possible answers: {len(words)}")

        guess = solver.guess(words)
        words.remove(guess)
        quiet_print(args.quiet, f"Guess: {guess}")
        tries += 1

        if args.non_interactive:
            response = get_response_non_interactive(args.word, guess)
            quiet_print(args.quiet, f"Response: {response}")
        else:
            response = get_response(args.len)
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
        logging.debug("Known letters: %s", known_letters)
        logging.debug("Search space: %s", search_space)
        words = trim_word_list_by_search_space(words, search_space, known_letters)
        logging.info("Words left: %s", len(words))
        logging.debug("Words: %s", words)
        quiet_print(args.quiet, "")  # New line for better readability

    if solution:
        stats['solved'] = stats.get('solved', 0) + 1
        stats['average_tries'] = \
            (stats.get('average_tries', 0) * (stats['solved'] - 1) + tries) / stats['solved']
        stats['tries'] = stats.get('tries', {})
        stats['tries'][solution] = tries
    else:
        quiet_print(args.quiet, "Failed to solve the Wordle!")
    save_stats(stats)
