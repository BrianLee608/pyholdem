#!/usr/bin/python
from collections import namedtuple, deque
import random
from players import Player, Bot
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
    

class Round():
    """Simulates a round and selects a winner(s)"""

    def __init__(self, table):
        self.live_players = [pl for pl in table.players if pl.chips > 0]
        self.players_alive = len(self.live_players)
        self.positions = [None] * self.players_alive
        self.btn = table.btn_pos
        self.deck = table.deck
        self.pot = [0]
        self.players_info = {}
        for pl in self.live_players:
            self.players_info[pl.name] = {'player_ref': pl,
                                          'contributed': 0,
                                          'folded': False}

    def start(self):
        self.deck.shuffle_deck()
        self.deal()
        self.play_preflop()

    def deal(self):
        """deals 2 * num_players cards"""

        for pl in self.live_players:
            pl.holecards = self.deck[self.deck.idx-2: self.deck.idx]
            self.deck.idx -= 2 
            
    def play_preflop(self):
        """Processes a round of betting for preflop."""
        
        if self.players_alive > 2:
            # btn is sb in heads up
            sb_pos = (self.btn + 1) % self.players_alive
            bb_pos = (self.btn + 2) % self.players_alive
        else:
            sb_pos = self.btn_pos
            bb_pos = (sb_pos + 1) % 2
        
        # collect blinds and update position list
        # ie positions = ['BTN', 'SB', 'BB', 'UTG', 'UTG+1']
        for i, pl in enumerate(self.live_players):
            if pl == self.live_players[sb_pos]:
                pl.bet(Table.SB, self.pot)
                self.positions[i] = 'BTN' if self.players_alive< 3 else 'SB'
            elif pl == self.live_players[bb_pos]:
                pl.bet(Table.BB, self.pot)
                self.positions[i] = 'BB'
            elif i == self.btn:
                self.positions[i] = 'BTN'
            elif self.players_alive > 3:
                utg = 'UTG' 
                if   i != (bb_pos + 1) % self.players_alive:
                    utg = 'UTG+'
                    shift = self.players_alive - 1 - bb_pos
                    utg += str(i-bb_pos-1) if i > bb_pos else str(i+shift)
                self.positions[i] = utg
       
        # initialize index(ie pos) of who is first to act
        if self.players_alive > 3:
            pos = self.positions.index('UTG')
        else:
            pos = self.positions.index('BTN')
        
        action_queue = [

        print(self.positions)
        

    def __str__(self):
        return '\n'.join(str(player) for player in self.live_players)


class Table():
    """Processes a poker game until only one player remains."""

    SB, BB = 1, 2

    def __init__(self, seats = 2, num_bb = 100):
        self.players = [Player(self.BB * num_bb, 'Hero')]
        self.players.extend([Bot(self.BB * num_bb) for _ in range(1, seats)])
        self.btn_pos = None
        self.deck = Deck()
    
    def remove_player(self, player_name):
        self.players = [p for p in self.players if p.name != player_name]
        pos = self.positions.index('BTN')
        
    def init_game(self):
        self.btn_pos = random.randint(0, len(self.players)- 1)

        print("Starting game!")
        # loop until 1 player standing
        while(len(self.players) > 1):
            round = Round(self)
            round.start()
            self.btn_pos = (self.btn_pos + 1) % len(self.players) - 1
            break
            # implement
        
    def __str__(self):
        return '\n'.join(str(player) for player in self.players)


def main():
    """Initializes a game of poker"""
    t = Table(seats = 6, num_bb = 100)
    t.init_game()

if __name__ == '__main__':
    main()
