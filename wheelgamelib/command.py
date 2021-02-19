import argparse

from .view import TextView
from .puzzle import Puzzle
from .wheel import WHEEL_1987_R3
from .contestant import Contestant
from .game import Game
from .controller import TextController

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("contestant1")
    p.add_argument("contestant2")
    p.add_argument("contestant3")
    p.add_argument(
        "--puzzle-file", type=argparse.FileType('r'),
        default="phrases.txt",
    )
    args = p.parse_args()

    wheel = WHEEL_1987_R3
    contestants = [
        Contestant(args.contestant1),
        Contestant(args.contestant2),
        Contestant(args.contestant3),
    ]

    puzzle_phrases = parse_puzzle_file(args.puzzle_file)
    game = None
    for phrase in puzzle_phrases:
        puzzle = Puzzle.from_phrase(phrase)
        if game:
            game.puzzle = puzzle
            game.state = "spin_wheel"
            for c in contestants:
                c.lose_next_turn = False
        else:
            game = Game(wheel, contestants, puzzle)
        view = TextView(game)
        controller = TextController(game, view)
        controller.launch()


def parse_puzzle_file(f):
    for line in f:
        line = line.strip()
        if line.startswith("#"):
            continue
        yield line
