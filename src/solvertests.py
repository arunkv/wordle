# pylint: skip-file
"""
This module contains unit tests for the Wordle solver implemented in the `solver.py` module.

Copyright 2024 Arun K Viswanathan
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""
import unittest

from constants import EXACT_MATCH, NO_MATCH, PARTIAL_MATCH
from responses import get_response_non_interactive


class SolverTestCase(unittest.TestCase):
    """
    The SolverTestCase class is a subclass of unittest.TestCase, which is used for testing the
    Wordle solver implemented in the `solver.py` module.

    Attributes:
        None

    Methods:
        test_guess_vs_word(self): A test function to compare the output of
        get_response_non_interactive with expected values.
    """
    def test_guess_vs_word(self):
        """
        A test function to compare the output of get_response_non_interactive with expected values.
        """

        self.assertEqual(''.join([NO_MATCH, NO_MATCH, PARTIAL_MATCH, PARTIAL_MATCH, NO_MATCH]), get_response_non_interactive('actor', 'slate'))
        self.assertEqual(''.join([PARTIAL_MATCH, PARTIAL_MATCH, NO_MATCH, NO_MATCH, NO_MATCH]), get_response_non_interactive('actor', 'taint'))
        self.assertEqual(''.join([EXACT_MATCH, EXACT_MATCH, NO_MATCH, EXACT_MATCH, PARTIAL_MATCH]), get_response_non_interactive('arrow', 'ardor'))
        self.assertEqual(''.join([EXACT_MATCH]*5), get_response_non_interactive('arrow', 'arrow'))
        self.assertEqual(''.join([NO_MATCH]*5), get_response_non_interactive('slate', 'quirk'))
        self.assertEqual(''.join([NO_MATCH, PARTIAL_MATCH, NO_MATCH, NO_MATCH, NO_MATCH]), get_response_non_interactive('dully', 'slate'))


if __name__ == '__main__':
    unittest.main()


