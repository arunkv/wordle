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
```

## Example

![Example Wordle game](./wordlegame.png)

```
❯ src/wordle.py -d words/word-unscrambler-words.txt -n -w sorry -s entropy
Round: 1
Current possible answers: 2309
Best guesses:
        - slate: (0.62)
        - sauce: (0.61)
        - slice: (0.61)
        - shale: (0.61)
        - saute: (0.60)
Guess: slate
Response: █████

Round: 2
Current possible answers: 56
Best guesses:
        - sorry: (0.57)
        - shiny: (0.57)
        - spiny: (0.54)
        - sunny: (0.53)
        - spicy: (0.52)
Guess: sorry
Response: █████
Wordle solved in 2 tries
```

## Statistics

### Letter Position Probability

This solver uses the probability of letters in each position to determine the best possible guess.

| Word List         | Words | Success Rate | Average Tries | Average Time Per Word (ms) |
|-------------------|-------|--------------|---------------|----------------------------|
| Wordle (original) | 2309  | 99.0%        | 3.76          | 3                          |
| ENABLE 2K         | 8672  | 87.4%        | 4.41          | 13                         |
| NYTimes Extended  | 14855 | 83.2%        | 4.57          | 22                         |

### Word Probability

This solver uses the probability of words in well known NLTK corpuses to determine the best possible guess.

| Word List         | Words | Success Rate | Average Tries | Average Time Per Word (ms) |
|-------------------|-------|--------------|---------------|----------------------------|
| Wordle (original) | 2309  | 98.1%        | 4.19          | 5                          |
| ENABLE 2K         | 8672  | 88.5%        | 4.66          | 15                         |
| NYTimes Extended  | 14855 | 83.2%        | 4.81          | 25                         |

### Entropy Lowering

This solver uses the entropy of the words to determine the best guess. The entropy score is calculated based on the
probability of resulting in greater number of exact or partial matches from a given guess. Computation of this
score is more time-consuming than the position probability solver.

| Word List         | Words | Success Rate | Average Tries | Average Time Per Word (ms) |
|-------------------|-------|--------------|---------------|----------------------------|
| Wordle (original) | 2309  | 98.8%        | 3.69          | 28                         |

_Timing from 2020 M1 MacBook Pro_

## CI Status

[![CodeQL](https://github.com/arunkv/wordle/actions/workflows/codeql.yml/badge.svg)](https://github.com/arunkv/wordle/actions/workflows/codeql.yml) [![Pylint](https://github.com/arunkv/wordle/actions/workflows/pylint.yml/badge.svg)](https://github.com/arunkv/wordle/actions/workflows/pylint.yml) [![Qodana](https://github.com/arunkv/wordle/actions/workflows/qodana_code_quality.yml/badge.svg)](https://github.com/arunkv/wordle/actions/workflows/qodana_code_quality.yml)

## License

Apache License 2.0
