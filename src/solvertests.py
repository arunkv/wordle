"""
This module contains unit tests for the Wordle solver implemented in the `solver.py` module.

Copyright 2024 Arun K Viswanathan
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""
import unittest

from solver import get_response_non_interactive


class SolverTestCase(unittest.TestCase):
    def test_guess_vs_word(self):
        """
        A test function to compare the output of get_response_non_interactive with expected values.
        """
        self.assertEqual('xxoox', get_response_non_interactive('actor', 'slate'))
        self.assertEqual('ooxxx', get_response_non_interactive('actor', 'taint'))
        self.assertEqual('==x=o', get_response_non_interactive('arrow', 'ardor'))
        self.assertEqual('=====', get_response_non_interactive('arrow', 'arrow'))
        self.assertEqual('xxxxx', get_response_non_interactive('slate', 'quirk'))
        self.assertEqual('xoxxx', get_response_non_interactive('dully', 'slate'))


if __name__ == '__main__':
    unittest.main()
