import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from Wordle import BinarySearch, playWordle
from WordleAssistant import containsAll, filter_by_feedback, getPossibleWords
from wordle_common import create_wordlist, feedback


ROOT = Path(__file__).resolve().parents[1]


class WordleTests(unittest.TestCase):
    def test_existing_wordlist(self):
        words = create_wordlist(ROOT / "Wordlist.txt")
        self.assertGreater(len(words), 100)
        self.assertEqual(words, sorted(set(words)))
        self.assertTrue(all(len(w) == 5 and len(set(w)) == 5 and not w.endswith("s") for w in words))
        self.assertIsNotNone(BinarySearch(words, words[-1]))

    def test_final_line_without_newline_and_unsorted_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "words.txt"
            path.write_text("zebra\napple\nzebra\ncrane", encoding="utf-8")
            self.assertEqual(create_wordlist(path), ["crane", "zebra"])

    def test_feedback_and_repeated_letters(self):
        self.assertEqual(feedback("crane", "crate"), "^^^x^")
        self.assertEqual(feedback("cigar", "array"), "x+x^x")
        self.assertEqual(feedback("cigar", "cigar"), "^^^^^")

    def test_feedback_filter_and_validation(self):
        candidates = {"crane", "crate", "slate"}
        self.assertEqual(filter_by_feedback(candidates, "crate", "^^^x^"), {"crane"})
        with self.assertRaises(ValueError):
            filter_by_feedback(candidates, "crate", "wrong")

    def test_assistant_constraints(self):
        words = ["crane", "crate", "slate"]
        self.assertEqual(containsAll(words, "aa"), set(words))
        self.assertEqual(getPossibleWords(words, {"c": 0}, "r", "t"), {"crane"})

    def test_game_rejects_bad_guess_and_wins(self):
        with patch("builtins.input", side_effect=[str(ROOT / "Wordlist.txt"), "bad", "crane"]):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                playWordle("crane")
        self.assertIn("Try again!", output.getvalue())
        self.assertIn("CONGRATULATIONS!", output.getvalue())

    def test_empty_wordlist_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.txt"
            path.write_text("apple\n", encoding="utf-8")
            with patch("builtins.input", return_value=str(path)):
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    playWordle()
        self.assertIn("no playable words", output.getvalue())


if __name__ == "__main__":
    unittest.main()
