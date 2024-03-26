# Interactive Wordle Solver

Solves the Wordle game interactively. 

_Wordle_ is a word puzzle in which the player has to guess a five-letter word within six attempts. After each guess, the player is given feedback on the letters that are correct and in the correct position, correct but in the wrong position, or incorrect.

NYTimes Wordle game: https://www.nytimes.com/games/wordle/index.html

## Installation
`pip install -r requirements.txt`

## Usage

`wordle.py [-h] [-D DICT] [-l LEN] [-t TRIES]`

Options:
```
  -h, --help              show this help message and exit
  -D DICT, --dict DICT    Dictionary file (default: NLTK words)
  -l LEN, --len LEN       Word length (default: 5)
  -t TRIES, --tries TRIES Maximum tries (default: 6)
```