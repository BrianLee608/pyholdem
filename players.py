#!/usr/bin/python

class Player():
    """Base model of a player. Extended by Bot class"""
    
    ALLOWED_ACTIONS = set(['check', 'raise', 'call', 'fold'])

    def __init__(self, starting_stack, name = None):
        self.chips = starting_stack
        self._holecards = [None] * 2 
        self.name = name or 'Unnamed'
        self.strongest_five = [None] * 5

    @property
    def holecards(self):
        return self._holecards

    @holecards.setter
    def holecards(self, cards):
        self._holecards[:] = cards[:]

    def receive_hand(self, cards):
        self._holecards[:] = cards[:]

    def __str__(self):
        cards = '{0}-{1}'.format(self.holecards[0], self.holecards[1])
        return '{0}: {1} ${2}'.format(self.name, cards, self.chips)

    def bet(self, amt, pot):
        """Attempts to contribute amt to a pot."""

        if amt > self.chips: 
            raise ValueError('Not enough chips')
        self.chips -= amt
        pot.accept_bet(self, amt)

    def check(self, pot):
        pot.accept_check(self)

    def fold(self, pot):
        pot.accept_fold(self)

    def call(self, pot):
        if pot.current_bet >= self.chips:
            self.shove(pot)
        else:
            self.bet(pot.current_bet, pot) 

    def shove(self, pot):
        self.bet(self.chips, pot)

    def act(self, pot):

        if pot.players[self]['latest_bet'] >= pot.current_bet:
            prompt = 'Pot: {0} Check or Raise'.format(pot.total)
        else:
            prompt = 'Pot: {0} Call {1}, Raise, or Fold'.format(pot.total, pot.current_bet)
        
        print(self.name + '\'s turn')
        print(self.holecards)
        valid_action = False
        while not valid_action:
            print(prompt)
            action = input('Enter action: ')
            valid_action = Player.verify_action(self, action, pot)
        
        action = action.lower().split(' ')
        if action[0] == 'check':
            self.check(pot)
        elif action[0] == 'fold':
            self.fold(pot)
        elif action[0] == 'raise':
            self.bet(action[1], pot)
        elif action[0] == 'call':
            self.call(pot)

        
    
    @staticmethod
    def verify_action(player, action, pot): 
        s = action.lower().split(' ')
        if s[0] not in Player.ALLOWED_ACTIONS:
            return False

        if pot.current_bet > 0:
            if s[0] == 'check':
                return False
            if s[0] == 'raise' and s[1] < pot.min_raise * 2:
                return False
        else:
            if s[0] == 'call':
                return False

        return True


class Bot(Player):
    """Extension of Player with AI strategies"""

    available_botnames = set(['Albert', 'Paul', 'Jen', 'Tom', 'Gavin', 'Kat']) 

    def __init__(self, starting_stack):
        self.chips = starting_stack
        self.name = self.available_botnames.pop()
        self._holecards = [None] * 2


