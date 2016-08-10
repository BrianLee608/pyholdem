#!/usr/bin/python
from collections import namedtuple
import random

class CardUtils():
    suit_unicodes = {'spades': '\u2660', 'diamonds': '\u2666', 
                    'clubs': '\u2663', 'hearts': '\u2665'}

    def __init(self):
       self.id = 1 
    
    @classmethod
    def as_unicode(cls, suit):
        return cls.suit_unicodes.get(suit)

# card data structure influenced from Fluent Python, Luciano Romalho(2015)
class Card(namedtuple('Card', 'rank suit')):
    """Wrapper class for namedtuple"""

    __slots__ = () #so instances take up memory sizeof tuple
    
    def __str__(self):
        return '{0}{1}'.format(self.rank, CardUtils.as_unicode(self.suit))


class Deck():
    """Basic 52 card deck"""    

    ranks = [str(r) for r in range(2,10)] + list('TJQKA')
    suits = 'spades diamonds clubs hearts'.split()
    
    def __init__(self):
        self._cards = [Card(r,s) for s in self.suits for r in self.ranks]
        self.idx = 52 # idx of top of deck

    def shuffle_deck(self):
        random.shuffle(self._cards)

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, idx):
        return self._cards[idx]

    def __setitem__(self, idx, card):
        self._cards[idx] = card

    def __str__(self):
        return ' '.join(str(card) for card in self._cards[0:self.idx])
    


