import math
import random

class Wheel:
    def __init__(self, fortunes):
        self.fortunes = fortunes
        self.length = len(fortunes)
        self.rotation = 0

    @property
    def fortune(self):
        idx = math.floor(self.rotation) % self.length
        return self.fortunes[idx]

    def spin(self, velocity, accelleration):
        assert(velocity > 0)
        assert(accelleration > 0)
        friction = 0.5 + random.triangular(-0.3, 0, 0.1)
        while True:
            accelleration = accelleration - friction
            velocity = velocity + accelleration
            if velocity <= 0:
                break
            for fortune in self._spin_step(velocity):
                yield velocity, fortune
        yield 0, self.fortune

    def _spin_step(self, velocity):
        """Yields the first fortune but not the last"""
        assert(velocity > 0)
        assert(self.rotation < self.length)
        destination = self.rotation + velocity
        
        current_idx = math.floor(self.rotation)
        destination_idx = math.floor(destination)
        while current_idx < destination_idx:
            fortune = self.fortunes[current_idx % self.length]
            yield fortune
            current_idx += 1

        self.rotation = destination
        while self.rotation >= self.length:
            self.rotation = self.rotation - self.length


class Money:
    event = "fortune_money"

    def __init__(self, amount):
        self.amount = amount

    def __str__(self):
        return '${:,}'.format(self.amount)


class Bankrupt:
    event = "fortune_bankrupt"

    def __str__(self):
        return "Bankrupt"


class LoseATurn:
    event = "fortune_lose_a_turn"

    def __str__(self):
        return "Lose a turn"


FORTUNES_1987_R3 = [
    Bankrupt(),
    Money(900),
    Money(3500),
    Money(250),
    Money(900),
    Money(200),
    Money(400),
    Money(550),
    Money(200),
    Money(500),
    Bankrupt(),
    Money(600),
    Money(200),
    Money(1000),
    Money(600),
    Money(300),
    Money(700),
    Money(450),
    Money(150),
    Money(800),
    LoseATurn(),
    Money(250),
    Money(400),
    Money(500),
]


WHEEL_1987_R3 = Wheel(FORTUNES_1987_R3)
