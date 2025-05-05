# -*- coding: utf-8 -*-
"""
This module provides functions to determine and process responses in the Wordle game.

Functions:
    get_response(is_non_interactive, word, guess, length): Determines the response based on the
    given word and guess.
    get_response_interactive(length): Prompts the user for a response and validates it.
    get_response_non_interactive(word, guess): Returns the response for a given word and guess.
    display_response(quiet, response): Displays the response to the user with colors.
    process_response(guess, response, search_space, known_letters, length): Processes the user's
    response to a guess.

Copyright 2024-2025 Arun K Viswanathan
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""
import logging
import string
from functools import lru_cache

from constants import EXACT_MATCH, NO_MATCH, PARTIAL_MATCH, RESPONSE_PROMPT, CHOOSE_GUESS, CHOOSE_GUESS_PROMPT


def get_response(is_non_interactive, word, guess, length):
    """
    A function that determines the response based on the given word and guess

    Parameters:
    - is_interactive: a boolean value indicating whether the game is interactive
    - word: the word to be compared with
    - guess: the guessed value to be compared with
    - length: the length of the word

    Returns:
    - response: the determined response based on the conditions
    """
    if is_non_interactive:
        response = get_response_non_interactive(word, guess)
    else:
        response = get_response_interactive(length)
    return response


def get_response_interactive(length):
    """
    Prompts the user for a response and validates it.

    This function repeatedly prompts the user for a response until a valid response is given. A
    valid response is either 'q', 'i', or a string of EXACT_MATCH, PARTIAL_MATCH, NO_MATCH
    characters of the same length as the provided `length` argument.

    Args:
        length (int): The expected length of the response.

    Returns:
        str: The user's response.
    """
    while True:
        response = input(RESPONSE_PROMPT)
        response = response.strip().lower()
        logging.info("Response: %s", response)
        if (all(char in {EXACT_MATCH, PARTIAL_MATCH, NO_MATCH} for char in response)
                and len(response) == length
                or response == 'i' or response == 'q' or response == CHOOSE_GUESS):
            break
        print("Invalid response. Please try again.")
    return response


def get_new_guess_interactive(length):
    """
    Prompts the user for a new guess and validates it.

    This function repeatedly prompts the user for a new guess until a valid guess is given. A
    valid guess is a string of lowercase letters of the same length as the provided `length`
    argument.

    Args:
        length (int): The expected length of the guess.

    Returns:
        str: The user's new guess.
    """
    while True:
        new_guess = input(CHOOSE_GUESS_PROMPT)
        new_guess = new_guess.strip().lower()
        logging.info("New guess entered: %s", new_guess)
        if len(new_guess) == length and all(char in string.ascii_lowercase for char in new_guess):
            break
        print("Invalid guess. Please try again.")
    return new_guess


@lru_cache(maxsize=128)
def get_response_non_interactive(word, guess):
    """
    Returns the response for a given word and guess.

    This function calculates the response for a given word and guess by comparing the letters at
    each position in the word and guess. It returns a string of EXACT_MATCH, PARTIAL_MATCH, and
    NO_MATCH characters indicating the matches between the word and guess.

    Args:
        word (str): The word to compare against.
        guess (str): The guess to compare with the word.

    Returns:
        str: The response string.
    """
    response = [NO_MATCH] * len(word)
    counted_pos = set()

    # Process exact matches first
    for i, guess_letter in enumerate(guess):
        if word[i] == guess_letter:
            response[i] = EXACT_MATCH
            counted_pos.add(i)

    # Process partial matches
    for i, guess_letter in enumerate(guess):
        if guess_letter in word and response[i] != EXACT_MATCH:
            positions = [i for i, letter in enumerate(word) if letter == guess_letter]
            for pos in positions:
                if pos not in counted_pos:
                    response[i] = PARTIAL_MATCH
                    counted_pos.add(pos)
                    break
    return ''.join(response)


def display_response(quiet, response):
    """
    Displays the response to the user with standard Wordle colors.

    Args:
        quiet (bool): A flag indicating whether to display the response quietly.
        response (str): The response string to display.

    Returns:
        None
    """
    if not quiet:
        print("Response: ", end='')
        for char in response:
            if char == EXACT_MATCH:
                print('🟩️', end='')
            elif char == PARTIAL_MATCH:
                print('🟨', end='')
            else:
                print('⬜️', end='')
        print()


def process_response(guess, response, search_space, known_letters, length):
    """
    Processes the user's response to a guess.

    This function updates the search space and known letters based on the user's response. It
    processes EXACT_MATCH responses first, then PARTIAL_MATCH responses, and finally NO_MATCH
    responses. For each type of response, it updates the known letters and the search space
    accordingly.

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
    # Process EXACT_MATCH responses first
    for i, response_letter in enumerate(response):
        if response_letter == EXACT_MATCH:
            known_letters.append(guess[i])
            search_space[i] = {guess[i]}

    # Then process PARTIAL_MATCH responses
    for i, response_letter in enumerate(response):
        if response_letter == PARTIAL_MATCH:
            known_letters.append(guess[i])
            search_space[i].discard(guess[i])

    # Finally, process NO_MATCH responses
    for i, response_letter in enumerate(response):
        if response_letter == NO_MATCH:
            search_space[i].discard(guess[i])
            other_exact_match_positions = set()
            other_partial_match_positions = set()
            for j, _ in enumerate(search_space):
                if j != i and guess[j] == guess[i]:
                    if response[j] == PARTIAL_MATCH:
                        other_partial_match_positions.add(j)
                    elif response[j] == EXACT_MATCH:
                        other_exact_match_positions.add(j)
            if not other_partial_match_positions:
                for j in set(range(length)) - {i} - other_exact_match_positions:
                    search_space[j].discard(guess[i])
