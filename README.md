# Wordle Solver

Solves the Wordle game interactively or optionally non-interactively. 

_Wordle_ is a word puzzle in which the player has to guess a five-letter word within six attempts. After each guess, 
the player is given feedback on the letters that are correct and in the correct position, correct but in the wrong 
position, or incorrect.

NYTimes Wordle game: https://www.nytimes.com/games/wordle/index.html

## Installation
`pip install -r requirements.txt`

## Usage

> `wordle.py [-h] [-D DICT] [-l LEN] [-t TRIES] [-n] [-w WORD] [-q]`

Interactive Wordle Solver

options:
  -h, --help              Show this help message and exit
  -D DICT, --dict DICT    Dictionary file (default: NLTK words)
  -l LEN, --len LEN       Word length (default: 5)
  -t TRIES, --tries TRIES Maximum tries (default: 6)
  -n, --non-interactive   Turn on non-interactive mode by providing the word to guess.
  -w WORD, --word WORD    The word to solve in non-interactive mode
  -q, --quiet             Turn off output

## Example
![Example Wordle game](./wordlegame.png)
```
❯ ./wordle.py
Guess: soree
Response (i for invalid word, x for no match, o for partial match, = for exact match)? xxxx=
Guess: ceile
Response (i for invalid word, x for no match, o for partial match, = for exact match)? i
Guess: alite
Response (i for invalid word, x for no match, o for partial match, = for exact match)? i
Guess: alate
Response (i for invalid word, x for no match, o for partial match, = for exact match)? xxxx=
Guess: binge
Response (i for invalid word, x for no match, o for partial match, = for exact match)? x=xx=
Guess: fifie
Response (i for invalid word, x for no match, o for partial match, = for exact match)? i
Guess: pixie
Response (i for invalid word, x for no match, o for partial match, = for exact match)? ==xx=
Guess: piece
Response (i for invalid word, x for no match, o for partial match, = for exact match)? ==xx=
Guess: pique
Response (i for invalid word, x for no match, o for partial match, = for exact match)? =====
Wordle solved in 6 tries
```

## CI Status
[![CodeQL](https://github.com/arunkv/wordle/actions/workflows/codeql.yml/badge.svg)](https://github.com/arunkv/wordle/actions/workflows/codeql.yml) [![Pylint](https://github.com/arunkv/wordle/actions/workflows/pylint.yml/badge.svg)](https://github.com/arunkv/wordle/actions/workflows/pylint.yml) [![Qodana](https://github.com/arunkv/wordle/actions/workflows/qodana_code_quality.yml/badge.svg)](https://github.com/arunkv/wordle/actions/workflows/qodana_code_quality.yml)

## License

Apache License 2.0

Includes [Enhanced North American Benchmark LExicon (ENABLE) 2K word list](http://wiki.puzzlers.org/dokuwiki/doku.php?id=solving:wordlists:about:enable_readme).
