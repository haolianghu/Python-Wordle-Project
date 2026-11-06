"""Shared word-list and feedback logic for the game and assistant."""

from collections import Counter


def create_wordlist(filename):
    """Load sorted, unique five-letter ASCII words without repeats or final s."""
    with open(filename, encoding="utf-8") as source:
        words = (line.strip() for line in source)
        return sorted({
            word for word in words
            if len(word) == 5 and word.isascii() and word.isalpha()
            and word.islower() and len(set(word)) == 5 and not word.endswith("s")
        })


def feedback(answer, guess):
    """Return Wordle-style feedback, assigning exact matches first."""
    if len(answer) != 5 or len(guess) != 5:
        raise ValueError("Answer and guess must both have five letters.")
    result = ["x"] * 5
    remaining = Counter()
    for i, (actual, guessed) in enumerate(zip(answer, guess)):
        if actual == guessed:
            result[i] = "^"
        else:
            remaining[actual] += 1
    for i, guessed in enumerate(guess):
        if result[i] != "^" and remaining[guessed]:
            result[i] = "+"
            remaining[guessed] -= 1
    return "".join(result)
