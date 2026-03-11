"""
This module contains unit tests for the Wordle solver implemented in the `solver.py` module.

Copyright 2024-2025 Arun K Viswanathan
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""
import string
import unittest

from constants import EXACT_MATCH, NO_MATCH, PARTIAL_MATCH
from responses import get_response_non_interactive, process_response
from solver import trim_word_list_by_search_space


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

        self.assertEqual(''.join([NO_MATCH, NO_MATCH, PARTIAL_MATCH, PARTIAL_MATCH, NO_MATCH]),
                         get_response_non_interactive('actor', 'slate'))
        self.assertEqual(''.join([PARTIAL_MATCH, PARTIAL_MATCH, NO_MATCH, NO_MATCH, NO_MATCH]),
                         get_response_non_interactive('actor', 'taint'))
        self.assertEqual(''.join([EXACT_MATCH, EXACT_MATCH, NO_MATCH, EXACT_MATCH, PARTIAL_MATCH]),
                         get_response_non_interactive('arrow', 'ardor'))
        self.assertEqual(''.join([EXACT_MATCH] * 5), get_response_non_interactive('arrow', 'arrow'))
        self.assertEqual(''.join([NO_MATCH] * 5), get_response_non_interactive('slate', 'quirk'))
        self.assertEqual(''.join([NO_MATCH, PARTIAL_MATCH, NO_MATCH, NO_MATCH, NO_MATCH]),
                         get_response_non_interactive('dully', 'slate'))
        self.assertEqual(''.join([NO_MATCH, NO_MATCH, PARTIAL_MATCH, NO_MATCH, PARTIAL_MATCH]),
                         get_response_non_interactive('abide', 'speed'))
        self.assertEqual(''.join([PARTIAL_MATCH, NO_MATCH, PARTIAL_MATCH, PARTIAL_MATCH, NO_MATCH]),
                         get_response_non_interactive('erase', 'speed'))
        self.assertEqual(''.join([EXACT_MATCH, NO_MATCH, EXACT_MATCH, NO_MATCH, NO_MATCH]),
                         get_response_non_interactive('steal', 'speed'))
        self.assertEqual(''.join([NO_MATCH, PARTIAL_MATCH, EXACT_MATCH, PARTIAL_MATCH, NO_MATCH]),
                         get_response_non_interactive('crepe', 'speed'))


class ProcessResponseTestCase(unittest.TestCase):
    """Tests for the process_response function."""

    def _make_search_space(self, length=5):
        return [set(string.ascii_lowercase) for _ in range(length)]

    def test_exact_match_locks_position(self):
        """An exact match should restrict the position to only that letter."""
        search_space = self._make_search_space()
        known_letters = []
        process_response('crane', EXACT_MATCH * 5, search_space, known_letters, 5)
        for i, letter in enumerate('crane'):
            self.assertEqual(search_space[i], {letter})
        self.assertEqual(known_letters, list('crane'))

    def test_partial_match_removes_from_position(self):
        """A partial match should remove the guessed letter from that position's search space."""
        search_space = self._make_search_space()
        known_letters = []
        # 'c' is partial at position 0
        process_response('crane', PARTIAL_MATCH + NO_MATCH * 4, search_space, known_letters, 5)
        self.assertNotIn('c', search_space[0])
        self.assertIn('c', known_letters)

    def test_no_match_removes_from_all_positions(self):
        """A no-match letter should be removed from every position in the search space."""
        search_space = self._make_search_space()
        known_letters = []
        # All letters are no match
        process_response('zzzzz', NO_MATCH * 5, search_space, known_letters, 5)
        for pos_set in search_space:
            self.assertNotIn('z', pos_set)

    def test_duplicate_letter_partial_then_no_match(self):
        """When a letter appears twice in the guess with partial then no-match,
        it should stay in known_letters but be removed from the no-match position."""
        search_space = self._make_search_space()
        known_letters = []
        # word='speed', guess='seeds': response is g y g y b (from existing tests)
        response = get_response_non_interactive('speed', 'seeds')
        process_response('seeds', response, search_space, known_letters, 5)
        # 's' exact at 0, so search_space[0] == {'s'}
        self.assertEqual(search_space[0], {'s'})
        # 's' appears in known_letters (from exact match at pos 0)
        self.assertIn('s', known_letters)
        # 's' should not be in search_space[4] (no match at pos 4)
        self.assertNotIn('s', search_space[4])

    def test_known_letters_cleared_each_call(self):
        """process_response should reset known_letters on each call."""
        search_space = self._make_search_space()
        known_letters = ['x', 'y', 'z']  # Pre-populated
        process_response('crane', NO_MATCH * 5, search_space, known_letters, 5)
        # known_letters should only contain letters from this call (none for all NO_MATCH)
        self.assertEqual(known_letters, [])


class TrimWordListTestCase(unittest.TestCase):
    """Tests for trim_word_list_by_search_space."""

    def _full_space(self, length=5):
        return [set(string.ascii_lowercase) for _ in range(length)]

    def test_no_constraints_returns_all(self):
        """With a full search space and no known letters, all words are returned."""
        words = ['crane', 'slate', 'audio']
        result = trim_word_list_by_search_space(words, self._full_space(), [])
        self.assertEqual(result, words)

    def test_locked_position_filters_correctly(self):
        """Words not matching a locked position should be removed."""
        words = ['crane', 'slate', 'crimp']
        search_space = self._full_space()
        search_space[0] = {'c'}  # First letter must be 'c'
        result = trim_word_list_by_search_space(words, search_space, [])
        self.assertIn('crane', result)
        self.assertIn('crimp', result)
        self.assertNotIn('slate', result)

    def test_known_letter_required(self):
        """Words missing a known letter should be removed."""
        words = ['crane', 'slate', 'audio']
        result = trim_word_list_by_search_space(words, self._full_space(), ['r'])
        self.assertIn('crane', result)
        self.assertNotIn('slate', result)
        self.assertNotIn('audio', result)

    def test_duplicate_known_letter(self):
        """Words must contain the required count of duplicate known letters."""
        words = ['speed', 'steed', 'crane']
        # Known letters require two 'e's
        result = trim_word_list_by_search_space(words, self._full_space(), ['e', 'e'])
        self.assertIn('speed', result)
        self.assertIn('steed', result)
        self.assertNotIn('crane', result)

    def test_empty_word_list(self):
        """An empty word list should return an empty list."""
        result = trim_word_list_by_search_space([], self._full_space(), [])
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
