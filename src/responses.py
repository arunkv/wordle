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

Copyright 2024 Arun K Viswanathan
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""
import logging

from constants import RESPONSE_PROMPT


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
    word_len = len(word)
    letters_left = word_len
    response = [''] * word_len

    # Process exact matches first
    for i, guess_letter in enumerate(guess):
        if word[i] == guess_letter:
            response[i] = '='
            letters_left -= 1

    # Process partial matches
    potential_partials = []
    for i, guess_letter in enumerate(guess):
        if response[i] == '':

            guess_letter_match_count = len([j for j, letter in enumerate(word)
                                            if letter == guess_letter and response[j] != '='])
            if guess_letter_match_count > 0:
                potential_partials.append((i, guess_letter, guess_letter_match_count))
            else:
                response[i] = 'x'
                letters_left -= 1
    potential_partial_index = 0
    while letters_left > 0:
        i, guess_letter, guess_letter_match_count = potential_partials[potential_partial_index]
        if guess_letter_match_count > 0:
            response[i] = 'o'
            for j, match in enumerate(potential_partials):
                if match[0] != i and match[1] == guess_letter:
                    potential_partials[j] = (match[0], match[1], match[2] - 1)
        else:
            response[i] = 'x'
        letters_left -= 1
        potential_partial_index += 1
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
            if char == '=':
                print('\033[92m\u2589\033[0m', end='')
            elif char == 'o':
                print('\033[93m\u2589\033[0m', end='')
            else:
                print('\033[91m\u2589\033[0m', end='')
        print()


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
