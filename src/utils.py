"""
This module provides utility functions for the Wordle game statistics project.

Functions:
    quiet_print(quiet, *args, **kwargs): Suppresses printing output when quiet mode is enabled.

Copyright 2024-2025 Arun K Viswanathan
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""


def quiet_print(quiet, *args, **kwargs):
    """
    A no-op function to suppress printing output.

    This function is used to suppress printing output when the quiet mode is enabled.

    Args:
        quiet (bool): Whether to suppress printing.
        *args: Positional arguments.
        **kwargs: Keyword arguments.

    Returns:
        None
    """
    if not quiet:
        print(*args, **kwargs)


def print_best_guesses(quiet, word_scores):
    """
    A function to display the best guesses based on word scores.

    Parameters:
    - quiet (bool): Flag to determine if the function should print output quietly.
    - word_scores (list): List of tuples containing word and corresponding score.

    Returns:
    - None
    """
    if not quiet:
        quiet_print(quiet, "Best guesses: ")
        for _, (word, score) in enumerate(word_scores[:5]):
            quiet_print(quiet, f"\t- {word}: ({score:.3f})")


def chunk_list(lst, num_chunks):
    """
    A function to split a list into chunks of size n.

    Parameters:
    - lst (list): The list to split into chunks.
    - n (int): The size of each chunk.

    Returns:
    - list: A list of chunks.
    """
    for i in range(0, len(lst), num_chunks):
        yield lst[i:i + num_chunks]
