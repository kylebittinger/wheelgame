import time

class TextView:
    wheel_speedup = 3

    def __init__(self, game):
        self.game = game

    def get_input(self, prompt):
        prompt = prompt + ": "
        result = None
        while not result:
            result = input(prompt)
            result = result.strip()
        return result

    def notify(self, message):
        print(message)
        print()

    def notify_found(self, num_found, letter):
        if num_found == 0:
            print("There are no {}'s".format(letter))
        if num_found == 1:
            print("There is one {}.".format(letter))
        else:
            print("There are {} {}'s.".format(num_found, letter))
        print()

    def show_contestants(self):
        for c in self.game.contestants:
            res = str(c)
            if c == self.game.contestant:
                res = res + " <---"
            print(res)
        print("Lifelines available:")
        if self.game.contestant.has_5050_lifeline:
            print("  50/50 choice")
        if self.game.contestant.has_friend_lifeline:
            print("  Phone a friend")
        if self.game.contestant.has_poll_lifeline:
            print("  Poll the audience")
        print()

    def show_spin(self, wheeldata):
        for velocity, fortune in wheeldata:
            if velocity > 0:
                t = 1 / (velocity * self.wheel_speedup)
                time.sleep(t)
            print(fortune)
        print()

    def show_5050(self):
        a, b = self.game.puzzle.choice_5050()
        print("50/50 choice: {} {}".format(a, b))
        print()
        
    def show_puzzle(self):
        words = self.game.puzzle.show()
        phrase = " ".join(words)
        print("*************************")
        print("  " + phrase)
        print("*************************")
