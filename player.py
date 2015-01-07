from card import Card
from deck import Deck

class Player:
    """
    This superclass class represents any player at a table with hole cards.
    """
    def __init__(self,name):
        self.name = name
        self.hole = 0
    def __str__(self):
        return 'Player '+str(self.name)+' has '+str(Card.int2pretty(self.hole))
    
    def deal(self,hole,deck):
        """
        Sets certain hole cards for the player. (Updates deck)
        """
        self.hole = Deck.draw(deck,hole)

class Villain(Player):
    """
    This subclass represents an opponent player in a poker game. As the game
    progresses, more information about the player, such as betting style,
    bluffing style, and style variation is gathered and updated here.
    """
    def __init__(self,name):
        Player.__init__(self,name)
        self.pmf = [1/52]*52 # Or however we want to represent card pmfs
        # For now, the only pmf is a uniform because I don't know how to sample
        # TBD: Here be the interesting numbers representing the 'style'


        
    
