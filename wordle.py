#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Wordle Solver

#    Copyright 2024 Arun K Viswanathan
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0

import argparse
import collections
import logging
import os
import string

import nltk

import constants

logging.basicConfig(filename=constants.LOG_FILE, filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_arguments():
    parser = argparse.ArgumentParser(description='Interactive Wordle Solver')
    parser.add_argument('-D', '--dict', type=str, help='Dictionary file (default: NLTK words)')
    parser.add_argument('-l', '--len', type=int, help='Word length (default: {})'.format(constants.DEFAULT_WORD_LENGTH))
    parser.add_argument('-t', '--tries', type=int, help='Maximum tries (default: {})'.format(constants.DEFAULT_TRIES))
    args = parser.parse_args()
    args.dict = args.dict or 'nltk'
    args.len = args.len or constants.DEFAULT_WORD_LENGTH
    args.tries = args.tries or constants.DEFAULT_TRIES
    return args


def get_word_list(word_list):
    try:
        if os.path.isfile(word_list):
            logging.info("Using custom dictionary: %s", word_list)
            with open(word_list) as f:
                return [line.strip() for line in f]
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


# Trim the word list by the provided search space, including known letters
def trim_word_list_by_search_space(word_list, search_space, known_letters):
    return [word for word in word_list if all(word[i] in letters for i, letters in enumerate(search_space))
            and set(known_letters).issubset(set(word))]


# Compute letter probabilities for each position in the word
def compute_letter_probabilities(words):
    letter_frequencies = [collections.Counter(word[i] for word in words) for i in range(len(words[0]))]
    letter_probabilities = [{letter: freq / len(words) for letter, freq in frequencies.items()} for frequencies in
                            letter_frequencies]
    return letter_probabilities


def compute_word_score(word, letter_probabilities):
    score = 0.0
    for i, letter in enumerate(word):
        score += letter_probabilities[i].get(letter, 0.0)

    return score


def compute_word_scores(words, letter_probabilities):
    # Compute the score for each word
    word_scores = [(word, compute_word_score(word, letter_probabilities)) for word in words]

    # Sort the words by score in descending order
    word_scores.sort(key=lambda x: x[1], reverse=True)

    return word_scores


def get_response(length):
    while True:
        response = input("Response (q quit, i invalid, x no match, o partial match, = exact match)? ")
        response = response.strip().lower()
        logging.info("Response: %s" % response)
        if (all(char in {'x', 'o', '='} for char in response) and len(response) == length
                or response == 'i' or response == 'q'):
            break
        else:
            print("Invalid response. Please try again.")
    return response


def solve(args):
    words = [word for word in get_word_list(args.dict) if len(word) == args.len and not word[0].isupper()]
    logging.info("Word list loaded with %s words", len(words))

    tries = 0
    search_space = [set(string.ascii_lowercase) for _ in range(args.len)]
    known_letters = set()
    while tries < args.tries:
        if len(words) == 0:
            print("No words left in the dictionary")
            break

        letter_probabilities = compute_letter_probabilities(words)
        word_scores = compute_word_scores(words, letter_probabilities)
        guess = word_scores[0][0]
        words.remove(guess)
        print("Guess: %s" % guess)
        logging.info("Guess: %s" % guess)
        tries += 1

        response = get_response(args.len)

        if response == 'q':  # Exit
            print("Aborting!")
            break

        if response == 'i':  # Try another word since Wordle didn't accept this word
            tries -= 1
            continue

        if response == '=' * args.len:  # Wordle solved
            print("Wordle solved in %s tries" % tries)
            break

        # Process '=' responses first
        for i, response_letter in enumerate(response):
            if response_letter == '=':
                known_letters.add(guess[i])
                search_space[i] = {guess[i]}

        # Then process 'o' responses
        for i, response_letter in enumerate(response):
            if response_letter == 'o':
                known_letters.add(guess[i])
                search_space[i].discard(guess[i])

        # Finally, process 'x' responses
        for i, response_letter in enumerate(response):
            if response_letter == 'x':
                search_space[i].discard(guess[i])
                other_exact_match_positions = set()
                other_partial_match_positions = set()
                for j, search_letters in enumerate(search_space):
                    if j != i and guess[j] == guess[i]:
                        if response[j] == 'o':
                            other_partial_match_positions.add(j)
                        elif response[j] == '=':
                            other_exact_match_positions.add(j)
                if not other_partial_match_positions:
                    for j in set(range(args.len)) - {i} - other_exact_match_positions:
                        search_space[j].discard(guess[i])

        logging.debug("Known letters: %s" % known_letters)
        logging.debug("Search space: %s" % search_space)
        words = trim_word_list_by_search_space(words, search_space, known_letters)
    logging.info("Words left: %s" % len(words))
    if tries >= args.tries:
        print("Failed to solve the Wordle. Words left: {}: {}".format(len(words), words[:10] if len(words) > 10 else words))
    else:
        print("Words left: {}: {}".format(len(words), words[:10] if len(words) > 10 else words))


if __name__ == '__main__':
    solve(parse_arguments())
