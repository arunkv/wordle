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

Copyright 2024-2025 Arun K Viswanathan
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""

import argparse
import cProfile
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
    parser = argparse.ArgumentParser(description='Wordle Solver')
    parser.add_argument('-d', '--dict', type=str, required=True, nargs='+',
                        help='Dictionary files')
    parser.add_argument('-l', '--len', type=int, default=constants.DEFAULT_WORD_LENGTH,
                        help=f'Word length (default: {constants.DEFAULT_WORD_LENGTH})')
    parser.add_argument('-t', '--tries', type=int, default=constants.DEFAULT_TRIES,
                        help=f'Maximum tries (default: {constants.DEFAULT_TRIES})')
    parser.add_argument('-n', '--non-interactive', action='store_true',
                        help='Turn on non-interactive mode by providing the word to guess')
    parser.add_argument('-w', '--word', type=str,
                        help='The word to solve in non-interactive mode')
    parser.add_argument('-c', '--continuous', action='store_true', default=False,
                        help='Continuous mode; uses all words in the dictionary')
    parser.add_argument('-s', '--solver', type=str, default='position',
                        choices=['position', 'word', 'entropy'],
                        help='Solver to use (default: position)')
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    parser.add_argument('-p', '--profile', action='store_true', help='Profile the code')
    args = parser.parse_args()
    if args.non_interactive:
        if not (args.word or args.continuous):
            parser.error('-n|--non-interactive requires -w|--word or -c|--continuous')
        elif args.word and args.continuous:
            parser.error("-w|--word and -c|--continuous arguments are mutually exclusive")
    elif args.word is not None:
        parser.error("-w|--word argument should not be used without -n|--non-interactive")
    args.len = args.len or constants.DEFAULT_WORD_LENGTH
    args.tries = args.tries or constants.DEFAULT_TRIES
    return args


if __name__ == '__main__':
    try:
        program_args = parse_arguments()
        PROFILER = None
        if program_args.profile:
            PROFILER = cProfile.Profile()
            PROFILER.enable()
        solve(parse_arguments())
        if program_args.profile:
            PROFILER.disable()
            PROFILER.print_stats(sort='cumtime')
    except KeyboardInterrupt:
        logging.info("Game interrupted by user")
        print()
