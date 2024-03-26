# Algorithm for solving Wordle

#    Copyright 2024 Arun K Viswanathan
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0

import collections
import logging
import string

from termcolor import colored

from wordlist import get_word_list


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


# Compute the score for a word given the individual letter probabilities
def compute_word_score(word, letter_probabilities):
    return sum(letter_probabilities[i].get(letter, 0.0) for i, letter in enumerate(word))


# Get the score for all words in the word list
def compute_word_scores(words, letter_probabilities):
    word_scores = [(word, compute_word_score(word, letter_probabilities)) for word in words]
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
            print(colored("Invalid response. Please try again."), 'red')
    return response


def solve(args):
    words = [word for word in get_word_list(args.dict) if len(word) == args.len and not word[0].isupper()]
    logging.info("Word list loaded with %s words", len(words))

    tries = 0
    search_space = [set(string.ascii_lowercase) for _ in range(args.len)]
    known_letters = set()
    letter_probabilities = compute_letter_probabilities(words)
    solved = False
    while tries < args.tries:
        if len(words) == 0:
            print(colored("No words left in the dictionary", "red", "on_white"))
            break

        word_scores = compute_word_scores(words, letter_probabilities)
        guess = word_scores[0][0]
        words.remove(guess)
        print("Guess: ", end="")
        print(colored(guess, 'blue', 'on_white'))
        logging.info("Guess: %s" % guess)
        tries += 1

        response = get_response(args.len)

        if response == 'q':  # Exit
            print(colored("Aborting!", "red"))
            break

        if response == 'i':  # Try another word since Wordle didn't accept this word
            tries -= 1
            continue

        if response == '=' * args.len:  # Wordle solved
            print(colored("Wordle solved in {} tries".format(tries), "green", "on_white"))
            solved = True
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
        print("Words left: {}: {}".format(len(words), words[:10] if len(words) > 10 else words))
    logging.info("Words left: %s" % len(words))
    if not solved:
        print(colored("Failed to solve the Wordle!", "red"))
