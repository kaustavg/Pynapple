from Core.deck import Deck
from Bot.player import *

class Game:
    """
    This class represents a single round of Poker. As the round progresses and
    more cards are put on the table, the Game object updates. At any state of
    the Game, a Monte Carlo Simulation can be performed to calculate odds.
    """
    def __init__(self,num_villains):
        self.nv = num_villains
        self.hero = Player(-1) # Player object representing hero
        self.vils = [Villain(i) for i in range(num_villains)] # List of villains
        self.n_vils = num_villains # Number of villains
        self.deck = Deck.new() # New deck
        self.comm = 0 # Community Cards
        self.n_comm = 0 # Number of community cards dealt

    def dealplayer(self,name,hole):
        """
        Deals certain hole cards to a given player and updates the deck.
        """
        if name==-1 or name == 'hero':
            self.hero.deal(hole,self.deck)
        else:
            self.vils[name].deal(hole,self.deck)

    def dealcomm(self,cards,n_cards=1):
        """
        Deals a community card specified by 'card' from the game deck and
        updates the deck.
        """
        self.comm += Deck.draw(self.deck,cards)
        self.n_comm += n_cards


        
        
