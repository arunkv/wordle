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
import logging

import constants
from solver import solve

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


if __name__ == '__main__':
    solve(parse_arguments())
