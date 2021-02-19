import functools
import operator
import random

from .error import (
    InvalidLetter, InvalidGuess,
)

class Puzzle:
    consonants = set("BCDFGHJKLMNPQRSTVWXZ")
    vowels = set("AEIOUY")
    
    def __init__(self, words):
        self.words = words
        self.already_guessed = set()
        self.n_found = 0

    @classmethod
    def from_phrase(cls, phrase):
        words = [PuzzleWord(word) for word in phrase.split()]
        return cls(words)

    def show(self):
        return [word.show() for word in self.words]

    def solve(self, guessed_phrase):
        guessed_words = guessed_phrase.split()
        return all(
            word.solve(guessed_word)
            for word, guessed_word
            in zip(self.words, guessed_words))

    def validate_vowel(self, letter):
        if letter not in self.vowels:
            raise InvalidGuess("{} is not a vowel.".format(letter))
        if letter in self.already_guessed:
            raise InvalidGuess("{} was already bought.".format(letter))

    def buy(self, letter):
        self.validate_vowel(letter)
        self.already_guessed.add(letter)
        n_found = 0
        for word in self.words:
            n_found += word.guess(letter)
        return n_found        

    def validate_guess(self, letter):
        if letter not in self.consonants:
            raise InvalidGuess("{} is not a consonant.".format(letter))
        if letter in self.already_guessed:
            raise InvalidGuess("{} was already guessed.".format(letter))

    def guess(self, letter):
        self.validate_guess(letter)
        self.already_guessed.add(letter)
        n_found = 0
        for word in self.words:
            n_found += word.guess(letter)
        self.n_found = n_found
        return n_found

    @property
    def unrevealed_letters(self):
        result = set()
        for word in self.words:
            result = result.union(word.unrevealed_letters)
        return result

    def choice_5050(self):
        good_guesses = self.consonants.intersection(
            self.unrevealed_letters)
        bad_guesses = self.consonants.difference(
            self.unrevealed_letters, self.already_guessed)
        good_guess = random.choice(list(good_guesses))
        bad_guess = random.choice(list(bad_guesses))
        res = [good_guess, bad_guess]
        random.shuffle(res)
        return res


class PuzzleWord:
    can_guess = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    can_show = set("-'")
    can_use = can_guess | can_show
    
    def __init__(self, letters):
        self.letters = letters
        self.is_revealed = [
            True if letter in self.can_show else False
            for letter in self.letters
        ]
        self.validate()

    def validate(self):
        for letter in self.letters:
            if not letter in self.can_use:
                template = (
                    "Can't use {} in puzzle.\n"
                    "Allowable characters: {}")
                message = template.format(
                    letter, "".join(self.can_use))
                raise InvalidLetter(message)

    @property
    def unrevealed_letters(self):
        return set(
            letter for letter, is_revealed
            in zip(self.letters, self.is_revealed)
            if not is_revealed)

    def show(self):
        return "".join(
            letter if letter_is_revealed else "_"
            for letter, letter_is_revealed
            in zip(self.letters, self.is_revealed))

    def guess(self, guessed_letter):
        n_found = 0
        for idx, letter in enumerate(self.letters):
            if letter == guessed_letter:
                self.is_revealed[idx] = True
                n_found += 1
        return n_found

    def solve(self, guessed_word):
        actual_word = "".join(self.letters)
        return guessed_word == actual_word
