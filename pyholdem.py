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
		
    def award_pot(self):
        """Awards pot total to the winner(s)"""
        pass

class Round():
    """Simulates a round and selects a winner(s)"""

    def __init__(self, table):
        self.players = [pl for pl in table.players if pl.chips > 0]
        self.deck = table.deck
        self.pot = Pot(self.players)
        self.btn = table.btn_idx

    def start(self):
        self.deck.shuffle_deck()
        self.deal()
        self.play_preflop()

    def deal(self):
        """deals 2 * num_players cards"""

        for pl in self.players:
            pl.receive_hand(self.deck[self.deck.idx-2: self.deck.idx])
            self.deck.idx -= 2 
    
    def prep_preflop_queue(self):
        """Prepares an action queue based on blind positions.

        Actions are processed from right to left so immediate actors go
        to the right of the queue. 
        I.e, 
        players = [D SB BB UTG UTG+1 UTG+2]
        then preflop queue will be arranged as:
        deque   = [BB SB D UTG+2 UTG+1 UTG]

        """

        return deque(self.players[self.btn::-1] + self.players[:self.btn:-1])

    def prep_postflop_queue(self):
        """Prepares action queue where BTN last to act (index 0)."""

        return deque([self.players[0]] + self.players[:0:-1])

    def play_preflop(self):
        """Processes a round of betting for preflop."""
        

        queue = self.prep_preflop_queue()
        
    def __str__(self):
        return '\n'.join(str(player) for player in self.players)


class Table():
    """Processes a poker game until only one player remains."""

    SB, BB = 1, 2

    def __init__(self, seats = 2, num_bb = 100):
        queue = [Player(self.BB * num_bb, 'Hero')]
        queue.extend([Bot(self.BB * num_bb) for _ in range(1, seats)])
        random.shuffle(queue) # randomize positions
        self.players = deque(queue, maxlen=seats)
        self.btn_idx = 1 if seats == 2 else 2
        self.deck = Deck()
        self.folded = []


    def del_dead_players(self):
	# todo: think of a better way to remove dead players
	# current method creates n new lists, where n = # of rounds
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
        print()
        print(self)


    def __str__(self):
        return '\n'.join(str(player) for player in self.players)


def main():
    """Initializes a game of poker"""
    t = Table(seats = 6, num_bb = 100)
    t.init_game()

if __name__ == '__main__':
    main()
