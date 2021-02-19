from .puzzle import (
    PuzzleWord, Puzzle,
    )

def test_puzzleword_unrevealed_letters():
    w = PuzzleWord("HELLO")
    assert(w.unrevealed_letters == set("HELLO"))
    w.guess("H")
    assert(w.unrevealed_letters == set("ELLO"))

def test_puzzle_unrevealed_letters():
    p = Puzzle.from_phrase("HELLO WORLD")
    assert(p.unrevealed_letters == set("HELLOWORLD"))
    p.guess("L")
    assert(p.unrevealed_letters == set("HEOWORD"))

def test_choice_5050():
    p = Puzzle.from_phrase("HELLO WORLD")
    choices = p.choice_5050()
    choices_in_p = [c for c in choices if c in "HELLOWORLD"]
    assert(len(choices_in_p) == 1)
