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
  -q, --quiet                                Quiet mode
```

## Example
![Example Wordle game](./wordlegame.png)
```
❯ dist/wordle -d wordle_words.txt -n -w sorry
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
The probabilistic solver solves the Wordle words (found in `wordle_words.txt`) in an average of 3.76 tries. On an M1 
MacBook Pro (2020), on average, the solver takes about 15 milliseconds to solve a word. Of the 2309 words in the word 
list, the solver is able to solve 2287 words (99% success rate) within the maximum of 6 tries. With the larger ENABLE
2K word list (8672 five-letter words), the solver is able to solve 7579 words (87.4% success rate) in an average of 
4.41 tries.


## CI Status
[![CodeQL](https://github.com/arunkv/wordle/actions/workflows/codeql.yml/badge.svg)](https://github.com/arunkv/wordle/actions/workflows/codeql.yml) [![Pylint](https://github.com/arunkv/wordle/actions/workflows/pylint.yml/badge.svg)](https://github.com/arunkv/wordle/actions/workflows/pylint.yml) [![Qodana](https://github.com/arunkv/wordle/actions/workflows/qodana_code_quality.yml/badge.svg)](https://github.com/arunkv/wordle/actions/workflows/qodana_code_quality.yml)

## License

Apache License 2.0
