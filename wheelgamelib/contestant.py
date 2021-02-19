from .error import NotEnoughMoney, LifelineError

class Contestant:
    def __init__(self, name):
        self.name = name
        self.money = 0
        self.lose_next_turn = False
        self.has_5050_lifeline = True
        self.has_friend_lifeline = True
        self.has_poll_lifeline = True

    def purchase_vowel(self):
        if self.money < 250:
            raise NotEnoughMoney()
        else:
            self.money -= 250

    def __str__(self):
        res = "{}: ${:,}".format(self.name, self.money)
        if self.lose_next_turn:
            res += "  LOSE A TURN"
        return res
