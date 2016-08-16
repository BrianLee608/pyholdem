#!/usr/bin/python
from collections import deque
from players import Player, Bot
from deck import Deck
import random

class Pot():
    """Encapsulates a pot structure and handles proper chip 
       distribution based on amount contributed by each player"""

    # Constants used to categorize each Player's most recent action
    NO_ACTION = 0
    FOLD = 1
    CHECK = 2
    CALL = 3
    RAISE = 4

    def __init__(self, players):
        self.total = 0
        self.current_bet = 0
        self.players = {pl:{} for pl in players}
        for pl in self.players:
            self.players[pl] = {'contributed': 0,
                               'latest_action': Pot.NO_ACTION,
                               'latest_bet': 0,
                               'folded': False,
                               'allin': False,
                               }
    
    def accept_check(self, player):
        self.players[player]['latest_action'] = Pot.CHECK
         
    def accept_fold(self, player):
        self.players[player]['latest_action'] = Pot.FOLD

    def accept_bet(self, player, amt):
        self.total += amt
        self.players[player]['contributed'] += amt
        self.players[player]['latest_bet'] = amt
        if amt > self.current_bet:
            self.current_bet = amt
            self.players[player]['latest_action'] = Pot.RAISE
        else:
            self.players[player]['latest_action'] = Pot.CALL
        
        if player.chips == 0:
            self.players[player]['allin'] = True

    def get_latest_action(self, player):
        """Returns the latest action committed by player"""

        return self.players[player]['latest_action']

    def award_pot(self):
        """Awards pot total to the winner(s)"""
        pass

class Round():
    """Simulates a round and selects a winner(s)"""

    def __init__(self, table):
        self.players = [pl for pl in table.players if pl.chips > 0]
        self.deck = table.deck
        self.pot = Pot(self.players)
        self.bb = table.bb_idx

    def start(self):
        self.deck.shuffle_deck()
        self.deal()
        self.play_preflop()

    def deal(self):
        """deals 2 * num_players cards"""

        for pl in self.players:
            pl.receive_hand(self.deck[self.deck.idx-2: self.deck.idx])
            self.deck.idx -= 2 
    
    def force_blind_post(self, pl, amt):
        pl.bet(amt, self.pot)

    def get_preflop_queue(self):
        """Prepares an action queue based on blind positions.

        Actions are processed from right to left so immediate actors go
        to the right of the queue. 
        I.e, 
        players = [D SB BB UTG UTG+1 UTG+2]
        then preflop queue will be arranged as:
        deque   = [BB SB D UTG+2 UTG+1 UTG]

        """
        
        queue = self.players[self.bb::-1] + self.players[:self.bb:-1]
        return deque(queue, maxlen = len(self.players))

    def get_postflop_queue(self):
        """Prepares action queue where BTN last to act (index 0)."""
        
        queue = self.players[0] + self.players[:0:-1]
        return deque(queue, maxlen = len(self.players))

    def process_bets(self, action_queue, street):
        """Processes a round of betting for a certain street"""
        
        acted = deque(maxlen = len(action_queue))
        print(street)

        while action_queue:
            pl = action_queue.pop()
            pl.act(self.pot)
            
            if self.pot.get_latest_action(pl) == Pot.RAISE:
                n = len(acted)
                action_queue.extendleft([acted.popleft() for _ in range(n)])
            
            acted.appendleft(pl)
            # continue implementing here. right now it infinitely loops
            # because the blinds will always have as latest_Action of raise
            # because Player.act hasn't been implemented yet!

    def play_preflop(self):
        """Processes a round of betting for preflop."""
        
        self.force_blind_post(self.players[self.bb-1], Table.SB)
        self.force_blind_post(self.players[self.bb], Table.BB)
        
        action_queue = self.get_preflop_queue()
        self.process_bets(action_queue, 'Preflop')
        
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
        self.bb_idx = 1 if seats == 2 else 2
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
