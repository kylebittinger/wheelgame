import random

from .error import (
    InvalidGuess, NotEnoughMoney, LifelineError,
    )

class TextController:
    def __init__(self, game, view):
        self.game = game
        self.view = view

    def launch(self):
        self.view.show_puzzle()
        while (self.game.state != "end"):
            getattr(self, self.game.state)()

    def spin_wheel(self):
        if self.game.contestant.lose_next_turn:
            self.view.notify(
                "{} loses a turn.".format(self.game.contestant.name))
            self.game.handle_event("lost_turn")
            return

        self.view.show_contestants()
        cmd = self.view.get_input("Roll two dice to spin wheel")
        toks = cmd.split()

        try:
            velocity = int(toks[0])
        except ValueError:
            velocity = random.randint(1, 6)
            velocity = velocity + 6
        try:
            accelleration = int(toks[1])
        except (ValueError, IndexError):
            accelleration = random.randint(1, 6)

        spindata = self.game.wheel.spin(velocity, accelleration)
        self.view.show_spin(spindata)
        self.game.handle_event("wheel_spun")

    def guess_letter(self):
        self.view.show_puzzle()
        self.view.show_contestants()
        
        while True:
            try:
                cmd = self.view.get_input(
                    "Guess letter or use lifeline")
                if cmd.startswith("50"):
                    self.game.handle_event("lifeline_5050")
                    self.view.show_5050()
                elif cmd.startswith("phone") or cmd.startswith("friend"):
                    self.game.handle_event("lifeline_friend")
                    self.view.notify("You may phone a friend.")
                elif cmd.startswith("poll") or cmd.startswith("audience"):
                    self.game.handle_event("lifeline_poll")
                    self.view.notify("Let's have the audience weigh in.")
                else:
                    letter = cmd[0]
                    num_found = self.game.puzzle.guess(letter)
                    self.view.notify_found(num_found, letter)
                    if num_found > 0:
                        self.view.show_puzzle()
                        self.game.handle_event("guess_correctly")
                    else:
                        self.game.handle_event("guess_incorrectly")
            except (InvalidGuess, LifelineError) as e:
                self.view.notify(e)
                continue
            break

    def vowel_or_solve(self):
        while True:
            self.view.show_contestants()
            cmd = self.view.get_input(
                "Buy a vowel, solve puzzle, or spin again")
            if cmd.startswith("solve"):
                return self.solve()
            if cmd.startswith("buy"):
                return self.buy_a_vowel()
            if cmd.startswith("spin"):
                self.game.handle_event("spin_again")
                return

    def solve(self):
        cmd = self.view.get_input("Solve the puzzle")
        if self.game.puzzle.solve(cmd):
            self.game.handle_event("solve_correctly")
            self.view.notify(
                "Correct!!! {} wins!".format(self.game.contestant.name))
        else:
            self.game.handle_event("solve_incorrectly")
            self.view.notify("Incorrect.")

    def buy_a_vowel(self):
        try:
            self.game.contestant.purchase_vowel()
        except NotEnoughMoney:
            self.view.notify("Not enough money.")
            return # game state does not change

        while True:
            try:
                cmd = self.view.get_input("Vowel to buy")
                vowel = cmd[0]
                num_found = self.game.puzzle.buy(vowel)
            except InvalidGuess as g:
                self.view.notify(g)
                contunue
            break

        self.view.notify(
            "There are {} {}'s.".format(num_found, vowel))
        self.view.show_puzzle()

