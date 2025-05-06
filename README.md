# Wordle Solver

Solves the Wordle game interactively or optionally non-interactively.

_Wordle_ is a word puzzle in which the player has to guess a five-letter word within six attempts. After each guess,
the player is given feedback on the letters that are correct and in the correct position, correct but in the wrong
position, or incorrect.

NYTimes Wordle game: https://www.nytimes.com/games/wordle/index.html

## Installation

`pip install -r requirements.txt`

## Usage

> `src/wordle.py [-h] -d DICT [DICT ...] [-l LEN] [-t TRIES] [-n] [-w WORD] [-c] [-q]`

### Options:

```
  -h, --help                                 Show this help message and exit
  -d DICT [DICT ...], --dict DICT [DICT ...] Dictionary files
  -l LEN, --len LEN                          Word length (default: 5)
  -t TRIES, --tries TRIES                    Maximum tries (default: 6)
  -n, --non-interactive                      Turn on non-interactive mode by providing the word to guess
  -w WORD, --word WORD                       The word to solve in non-interactive mode
  -c, --continuous                           Continuous mode; uses all words in the dictionary
  -s, --solver                               Solver to use (default: position)
  -q, --quiet                                Quiet mode
  -p, --profile                              Profile the code (for debugging)
```

## Example

![Example Wordle game](./wordlegame.png)

```
❯ src/wordle.py -d words/wordle-nyt-words-14855.txt -n -w sorry -s entropy
Round: 1
Current possible answers: 14855
Best guesses:
        - tares: (4.305)
        - lares: (4.270)
        - rales: (4.256)
        - teras: (4.254)
        - ranes: (4.250)
Guess: tares
Response: ⬜️⬜️🟩️⬜️🟨

Round: 2
Current possible answers: 39
Best guesses:
        - scrog: (2.514)
        - gorsy: (2.464)
        - siroc: (2.428)
        - sprog: (2.421)
        - sirup: (2.412)
Guess: scrog
Response: 🟩️⬜️🟩️🟨⬜️

Round: 3
Current possible answers: 4
Best guesses:
        - sorbo: (1.386)
        - sorbi: (1.040)
        - sordo: (1.040)
        - sorry: (0.562)
Guess: sorbo
Response: 🟩️🟩️🟩️⬜️⬜️

Round: 4
Current possible answers: 1
Best guesses:
        - sorry: (0.000)
Guess: sorry
Response: 🟩️🟩️🟩️🟩️🟩️
Wordle solved in 4 tries
Wordle Game Statistics
----------------------
Games Played: 2
Games Solved: 2
Average Tries: 4.00
Success Rate: 100.0 %
Solve Time Per Game: 9226 ms
```

## Statistics

### Letter Position Probability

This solver uses the probability of letters in each position to determine the best possible guess.

| Word List         | Words | Success Rate | Average Tries | Average Time Per Word (ms) |
|-------------------|-------|--------------|---------------|----------------------------|
| Wordle (original) | 2315  | 99.0%        | 3.78          | 3                          |
| NYTimes Extended  | 14855 | 83.2%        | 4.57          | 21                         |

### Word Probability

This solver uses the probability of words in well known NLTK corpuses to determine the best possible guess.

| Word List         | Words | Success Rate | Average Tries | Average Time Per Word (ms) |
|-------------------|-------|--------------|---------------|----------------------------|
| Wordle (original) | 2315  | 98.1%        | 4.19          | 4                          |
| NYTimes Extended  | 14855 | 83.2%        | 4.81          | 25                         |

### Entropy Lowering

This solver uses the entropy of the words to determine the best guess. The entropy score is calculated based on the
probability of resulting in greater number of exact or partial matches from a given guess. Computation of this
score is more time-consuming than the position probability solver.

| Word List         | Words | Success Rate | Average Tries | Average Time Per Word (ms) |
|-------------------|-------|--------------|---------------|----------------------------|
| Wordle (original) | 2315  | 99.6%        | 3.57          | 14                         |
| NYTimes Extended  | 14855 | 90.5%        | 4.29          | 252                        |


_Timing from 2020 M1 MacBook Pro (8 cores)_

## CI Status

[![CodeQL](https://github.com/arunkv/wordle/actions/workflows/codeql.yml/badge.svg)](https://github.com/arunkv/wordle/actions/workflows/codeql.yml) [![Pylint](https://github.com/arunkv/wordle/actions/workflows/pylint.yml/badge.svg)](https://github.com/arunkv/wordle/actions/workflows/pylint.yml) 

## License

Apache License 2.0
