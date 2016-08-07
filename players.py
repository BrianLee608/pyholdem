#!/usr/bin/python

class Player():
    """Base model of a player. Extended by Bot class"""
    
    def __init__(self, starting_stack, name = None):
        self.chips = starting_stack
        self.holecards = None 
        self.name = name or 'Unnamed'

    def __str__(self):
        cards = '{0}-{1}'.format(self.holecards[0], self.holecards[1])
        return '{0}: {1} ${2}'.format(self.name, cards, self.chips)

    def bet(self, amt, pot):
        """Attempts to contribute amt to a pot.

        Note, pot is an instance variable of a Round object
        and is structured as a list in order to mutate it
        """

        if amt > self.chips: 
            raise ValueError('Not enough chips')
        self.chips -= amt
        pot[0] += amt

    def check(self):
        pass

    def fold(self):
        pass

    def call(self, amt, pot):
        self.bet(amt, pot)        

    def shove(self, pot):
        self.bet(self.chips, pot)

    def act(self):
        pass


class Bot(Player):
    """Extension of Player with AI strategies"""

    available_botnames = set(['Albert', 'Paul', 'Jen', 'Tom', 'Gavin']) 

    def __init__(self, starting_stack):
        self.chips = starting_stack
        self.name = self.available_botnames.pop()
        self.holecards = None


