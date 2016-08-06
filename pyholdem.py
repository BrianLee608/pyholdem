#!/usr/bin/python
from collections import namedtuple
import random 
from util import CardUtils

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
        self.players = [Player(self.BB * num_bb, 'Hero')]
        self.players.extend([Bot(self.BB * num_bb) for _ in range(1, seats)])
        self.btn_pos = None
        self.positions = [None] * seats
        self.deck = Deck()

    def deal(self):
        """deals 2 * num_players cards and decrements top of deck idx"""

        for player in self.players:
            player.holecards = self.deck[self.deck.idx-2: self.deck.idx]
            self.deck.idx -= 2 

    def play_preflop(self):
       
        # collect blinds and update position[] 
        if len(self.players) > 2:
            sb_pos = (self.btn_pos+1) % len(self.players)
            bb_pos = (self.btn_pos+2) % len(self.players)
        else:
            sb_pos = self.btn_pos
            bb_pos = (sb_pos+1) % 2
        print(self.btn_pos)
        print(sb_pos)
        for i, player in enumerate(self.players):
            if player == self.players[sb_pos]:
                player.chips -= Table.SB
                self.positions[i] = 'BTN' if len(self.players) < 3 else 'SB'
            elif player == self.players[bb_pos]:
                player.chips -= Table.BB
                self.positions[i] = 'BB'
            elif i == self.btn_pos:
                self.positions[i] = 'BTN'
            elif len(self.players) > 3:
                utg = 'UTG' 
                if   i != (bb_pos + 1) % len(self.players):
                    utg = 'UTG+'
                    shift = len(self.players) - 1 - bb_pos
                    utg += str(i-bb_pos-1) if i > bb_pos else str(i+shift)
                self.positions[i] = utg
        
        print(self.positions)
        

    def init_game(self):
        self.btn_pos = random.randint(0, len(self.players)- 1)

        print("Starting game!")
        # loop until 1 player standing
        while(len(self.players) > 1):
            self.deck.shuffle_deck()
            self.deal()
            self.play_preflop()
            break
            # implement
        
    def __str__(self):
        return '\n'.join(str(player) for player in self.players)


def main():
    """Initializes a game of poker"""
    t = Table(seats = 6, num_bb = 100)
    t.init_game()
    print(t)

if __name__ == '__main__':
    main()
