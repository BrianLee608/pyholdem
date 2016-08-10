#!/usr/bin/python
from collections import deque
from players import Player, Bot
from deck import Deck
import random

class Pot():
    """Encapsulates a pot structure and handles proper chip distribution based
        on amount contributed by each player"""

    def __init__(self, players):
        self.total = 0
        self.contributions = {pl:0 for pl in players}
                                          
    
    def accept_bet(self, player, amt):
        self.total += amt
        self.contributions[player] += amt


class Round():
    """Simulates a round and selects a winner(s)"""

    def __init__(self, table):
        self.players = [pl for pl in table.players if pl.chips > 0]
        self.deck = table.deck
        self.pot = Pot(self.players)

    def start(self):
        self.deck.shuffle_deck()
        self.deal()
        self.play_preflop()

    def deal(self):
        """deals 2 * num_players cards"""

        for pl in self.players:
            pl.receive_hand(self.deck[self.deck.idx-2: self.deck.idx])
            self.deck.idx -= 2 
            
    def play_preflop(self):
        """Processes a round of betting for preflop."""
        
        queue = [] # prepare a queue of players to act in order


    def __str__(self):
        return '\n'.join(str(player) for player in self.players)


class Table():
    """Processes a poker game until only one player remains."""

    SB, BB = 1, 2

    def __init__(self, seats = 2, num_bb = 100):
        queue = [Player(self.BB * num_bb, 'Hero')]
        queue.extend([Bot(self.BB * num_bb) for _ in range(1, seats)])
        random.shuffle(queue) # randomize positions
        self.players = deque(queue)
        self.deck = Deck()
        self.folded = []

    def del_dead_players(self):
        self.players = [p for p in self.players if p.chips > 0]
        
    def init_game(self):
        print(self)
        print()
        print("Starting game!")
        # loop until 1 player standing
        while(len(self.players) > 1):
            round = Round(self)
            round.start()
            # need to handle btn passing when players eliminated
            #self.btn_pos = (self.btn_pos + 1) % len(self.players) - 1
            break
            # implement
        print(self)


    def __str__(self):
        return '\n'.join(str(player) for player in self.players)


def main():
    """Initializes a game of poker"""
    t = Table(seats = 6, num_bb = 100)
    t.init_game()

if __name__ == '__main__':
    main()
