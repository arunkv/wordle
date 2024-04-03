# -*- coding: utf-8 -*-
"""
Stats Module

This module contains functions to load and save game statistics for the Wordle game. The statistics
are stored in a JSON file.

The load_stats function attempts to open and read a JSON file containing the game statistics. If
the file does not exist or cannot be decoded, it returns an empty dictionary.

The save_stats function attempts to open and write to a JSON file containing the game statistics.
The statistics are provided as a dictionary and are written to the file in JSON format.

This module is part of a Wordle solver game and is used to keep track of game statistics such as
the number of games played, the number of games solved, and the average number of tries to solve
a game.

Copyright 2024 Arun K Viswanathan
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""

import json

from constants import WORDLE_STATS_FILE, FAILURE_PROMPT
from utils import quiet_print


def load_stats():
    """
    Loads the Wordle game statistics from a file.

    This function attempts to open and read a JSON file containing the game statistics. If the file
    does not exist or cannot be decoded, it returns an empty dictionary.

    Returns:
        dict: A dictionary containing the game statistics, or an empty dictionary if the file does
              not exist or cannot be decoded.
    """
    try:
        with open(WORDLE_STATS_FILE, 'r', encoding='utf-8') as stats_file:
            return json.load(stats_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_stats(stats):
    """
    Saves the Wordle game statistics to a file.

    This function attempts to open and write to a JSON file containing the game statistics.
    The statistics are provided as a dictionary and are written to the file in JSON format.

    Args:
        stats (dict): A dictionary containing the game statistics.

    Returns:
        None
    """
    with open(WORDLE_STATS_FILE, 'w', encoding='utf-8') as stats_file:
        json.dump(stats, stats_file, indent=4)


def update_solved_stats(stats, solution, tries):
    """
    Updates the statistics dictionary with information about a newly solved problem.

    Parameters:
    - stats (dict): A dictionary containing statistics about solved problems.
    - solution (str): The solution to the newly solved problem.
    - tries (int): The number of tries it took to solve the problem.
    """
    stats['solved'] = stats.get('solved', 0) + 1
    stats['average_tries'] = \
        (stats.get('average_tries', 0) * (stats['solved'] - 1) + tries) / stats['solved']
    stats['tries'] = stats.get('tries', {})
    stats['tries'][solution] = tries


def update_failed_stats(args, stats):
    """
    Update the 'failed' stats with the given arguments and statistics.

    Parameters:
    args (argparse.Namespace): The arguments for the function.
    stats (dict): The statistics to update.

    Returns:
    None
    """
    stats['failed'] = stats.get('failed', [])
    if args.non_interactive:
        stats['failed'].append(args.word)
    else:
        word = input(FAILURE_PROMPT)
        if word:
            stats['failed'].append(word)
    stats['failed'] = list(set(stats['failed']))  # Remove duplicates


def finalize_stats(args, stats, solution, tries):
    """
    Update the statistics based on the solution and number of tries.

    Parameters:
        args (argparse.Namespace): The arguments passed to the function.
        stats (dict): The current statistics dictionary.
        solution (str): The solution string.
        tries (int): The number of tries it took to solve the solution.

    Returns:
        None
    """
    if solution:
        update_solved_stats(stats, solution, tries)
    else:
        quiet_print(args.quiet, "Failed to solve the Wordle!")
        update_failed_stats(args, stats)

    save_stats(stats)
