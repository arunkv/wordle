"""
This module provides utility functions for the Wordle game statistics project.

Functions:
    quiet_print(quiet, *args, **kwargs): Suppresses printing output when quiet mode is enabled.

Copyright 2024 Arun K Viswanathan
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
