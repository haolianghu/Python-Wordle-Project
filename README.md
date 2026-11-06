# Wordle game and assistant

A command-line five-letter guessing game and a companion candidate filter,
implemented using the Python standard library. The included `Wordlist.txt`
provides the game's words; there is no Excel data source in this repository.

## Run

From the repository directory, with Python 3:

```bash
python Wordle.py
python WordleAssistant.py
python -m unittest discover -s tests -v
```

When prompted for the word-list file, enter `Wordlist.txt` or a path to your own
UTF-8 file with one lowercase word per line. Both programs use the same filtered
list: five ASCII letters, no repeated letters, and no final `s`. This simplified
game therefore has a smaller vocabulary than the official game. The loader
sorts and deduplicates entries and accepts a final line without a newline.

The game accepts six valid guesses and reports `^` for the right position, `+`
for a letter in a different position, and `x` for an absent letter. Invalid
guesses do not consume an attempt.

The assistant first asks for known positions (zero-based), required letters,
and excluded letters. Optionally enter prior guesses and their five feedback
symbols to narrow the results further, including positional exclusions implied
by `+`. Press Enter instead of a guess to finish. Results are limited to the
same filtered word list; an empty result may mean the answer is not in that
list or that the supplied clues conflict. This is an independent educational
project, not the official Wordle game.
