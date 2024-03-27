#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wordle Solver

This module provides an interactive Wordle solver. It parses command-line arguments, sets up
logging, and calls the `solve` function from the `solver` module to start the game.

The command-line arguments are:
- `-D` or `--dict`: The dictionary file to use. The default is NLTK words.
- `-l` or `--len`: The length of the words to use. The default is the value of
`constants.DEFAULT_WORD_LENGTH`.
- `-t` or `--tries`: The maximum number of tries. The default is the value of
`constants.DEFAULT_TRIES`.

This module is meant to be run as a script. It does not provide any functions or classes that can
be imported into other modules.

Copyright 2024 Arun K Viswanathan
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""

import argparse
import logging

import constants
from solver import solve

logging.basicConfig(filename=constants.LOG_FILE, filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_arguments():
    """
    Parses the command-line arguments for the Wordle solver.

    The command-line arguments are:
    - `-D` or `--dict`: The dictionary file to use. The default is NLTK words.
    - `-l` or `--len`: The length of the words to use. The default is the value of
    `constants.DEFAULT_WORD_LENGTH`.
    - `-t` or `--tries`: The maximum number of tries. The default is the value of
    `constants.DEFAULT_TRIES`.

    Returns:
        argparse.Namespace: The parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description='Interactive Wordle Solver')
    parser.add_argument('-D', '--dict', type=str, help='Dictionary file (default: NLTK words)')
    parser.add_argument('-l', '--len', type=int,
                        help=f'Word length (default: {constants.DEFAULT_WORD_LENGTH})')
    parser.add_argument('-t', '--tries', type=int,
                        help=f'Maximum tries (default: {constants.DEFAULT_TRIES})')
    args = parser.parse_args()
    args.dict = args.dict or 'nltk'
    args.len = args.len or constants.DEFAULT_WORD_LENGTH
    args.tries = args.tries or constants.DEFAULT_TRIES
    return args


if __name__ == '__main__':
    solve(parse_arguments())
