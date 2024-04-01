# -*- coding: utf-8 -*-
"""
Constants for Wordle Solver

This module defines several constants used throughout the Wordle solver application, including:
- `DEFAULT_WORD_LENGTH`: The default length of the words to use in the game.
- `DEFAULT_TRIES`: The default maximum number of tries; 1 more than the default word length.
- `LOG_FILE`: The name of the file where logs are written.
- `WORDLE_STATS_FILE`: The name of the file where game statistics are stored.

These constants can be imported into other modules as needed.

Copyright 2024 Arun K Viswanathan
Licensed under the Apache License, Version 2.0
"""
# Constants

#    Copyright 2024 Arun K Viswanathan
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0

DEFAULT_WORD_LENGTH = 5
DEFAULT_TRIES = DEFAULT_WORD_LENGTH + 1
LOG_FILE = 'wordle.log'
WORDLE_STATS_FILE = 'wordle_stats.json'
RESPONSE_PROMPT = "Response (q quit, i invalid, x no match, o partial match, = exact match)? "
FAILURE_PROMPT = "Please provide the correct word: "
