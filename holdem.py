#!/usr/bin/python

from collections import namedtuple
import random 

# card data structure influenced from Fluent Python, Luciano Romalho(2015)
class Card(namedtuple('Card', 'rank suit')):
    """Wrapper class for namedtuple"""

    __slots__ = () #so instances take up memory sizeof tuple
    
    def __str__(self):
        return '{0}{1}'.format(self.rank, self.suit[0])

class Deck():
    """Basic 52 card deck"""    

    ranks = [str(r) for r in range(2,10)] + list('TJQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(r,s) for s in self.suits for r in self.ranks]
    
    def shuffle_deck(self):
        random.shuffle(self._cards)

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, idx):
        return self._cards[idx]

    def __setitem__(self, idx, card):
        self._cards[idx] = card
    

class Player():
    """Base model of a player. Extended by Bot class"""
    
    def __init__(self, starting_stack, name = None):
        self.chips = starting_stack
        self.holecards = None 
        self.name = name or 'Unnamed'

    def __str__(self):
        cards = '{0}-{1}'.format(self.holecards[0], self.holecards[1])
        return '{0}: {1} ${2}'.format(self.name, cards, self.chips)

    def act(self):
        pass


class Bot(Player):
    """Extension of Player with AI strategies"""

    available_botnames = set(['Albert', 'Paul', 'Jen', 'Tom', 'Gavin']) 

    def __init__(self, starting_stack):
        self.chips = starting_stack
        self.name = self.available_botnames.pop()
        self.holecards = None


class Table():
    """Processes a poker game"""

    SB, BB = 1, 2

    def __init__(self, seats = 2, num_bb = 100):
        self.players = [Player(self.BB * num_bb, 'Human')]
        self.players.extend([Bot(self.BB * num_bb) for _ in range(1, seats)])
            
    def deal(self, deck, idx):
        for player in self.players:
            player.holecards = deck[-2:]
            deck = deck[:-2]

    def init_game(self):
        deck = Deck()
        action_idx = random.randint(0, len(self.players) - 1)        
        
        print("Starting game!")
        while(len(self.players) > 1):
            deck.shuffle_deck()
            deck_idx = len(deck) - 1
            self.deal(deck, deck_idx)
            break
            # implement
        
    def __str__(self):
        return '\n'.join(str(player) for player in self.players)


if __name__ == '__main__':
    
    t = Table(seats = 4, num_bb = 100)
    t.init_game()
    print(t)
