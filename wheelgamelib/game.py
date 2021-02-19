import itertools

from .error import LifelineError

class Game:
    event_next_state = {
        # Events that advance to next state of play
        "fortune_money": "guess_letter",
        "guess_correctly": "vowel_or_solve",
        "solve_correctly": "end",
        "spin_again": "spin_wheel",

        # Lifeline events
        "lifeline_5050": "guess_letter",
        "lifeline_friend": "guess_letter",
        "lifeline_poll": "guess_letter",
        
        # Events that advance to next player
        "fortune_bankrupt": "spin_wheel",
        "fortune_lose_a_turn": "spin_wheel",
        "guess_incorrectly": "spin_wheel",
        "solve_incorrectly": "spin_wheel",
        "lost_turn": "spin_wheel",
    }

    failure_events = set([
        "fortune_bankrupt",
        "fortune_lose_a_turn",
        "guess_incorrectly",
        "solve_incorrectly",
        "lost_turn",
    ])
    
    def __init__(self, wheel, contestants, puzzle):
        self.wheel = wheel
        self.contestants = contestants
        self.puzzle = puzzle
        self.state = "spin_wheel"
        self._contestant_iter = itertools.cycle(self.contestants)
        self.contestant = next(self._contestant_iter)

    def handle_event(self, event):
        if event == "wheel_spun":
            event = self.wheel.fortune.event

        methodname = "handle_event_" + event
        if hasattr(self, methodname):
            getattr(self, methodname)()

        self.state = self.event_next_state[event]
        if event in self.failure_events:
            self.contestant = next(self._contestant_iter)

    def handle_event_lifeline_5050(self):
        if not self.contestant.has_5050_lifeline:
            raise LifelineError("50/50 choice not available.")
        self.contestant.has_5050_lifeline = False

    def handle_event_lifeline_friend(self):
        if not self.contestant.has_friend_lifeline:
            raise LifelineError("Phone a friend not available.")
        self.contestant.has_friend_lifeline = False

    def handle_event_lifeline_poll(self):
        if not self.contestant.has_poll_lifeline:
            raise LifelineError("Poll the audience not available.")
        self.contestant.has_poll_lifeline = False
            
    def handle_event_fortune_bankrupt(self):
        self.contestant.money = 0

    def handle_event_fortune_lose_a_turn(self):
        self.contestant.lose_next_turn = True

    def handle_event_lost_turn(self):
        self.contestant.lose_next_turn = False

    def handle_event_guess_correctly(self):
        self.contestant.money += self.wheel.fortune.amount * self.puzzle.n_found
