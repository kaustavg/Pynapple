import random as rand
class Deck:
    """
    This class creates a Deck and can deal Cards.
    A deck is simply a list of ints representing each card.
    The "deal" method will pop a given element from the deck, but the "pickn"
    method will randomly select n cards from the deck and return them in a hand
    without removing those cards from the deck. Thus, "draw" is useful when
    actually simulating a game and updating the deck, while "pickn" is useful
    for running Monte Carlo Simulations.
    """
    FULLDECK = list(map(lambda x: 1<<x, range(52)))

    @staticmethod
    def new():
        """
        Returns a new deck that is NOT SHUFFLED.
        """
        return Deck.FULLDECK

    @staticmethod
    def draw(deck,cardint):
        """
        Removes cards from the deck (updating the deck) and returns cardint.
        """
        allcards = cardint
        while cardint != 0:
            deck.remove(cardint & -cardint)
            cardint &= cardint-1

        return allcards

    @staticmethod
    def pickn(deck,n=1):
        """
        Returns n-card int from a given deck WITHOUT UPDATING THE DECK. This is
        useful for Monte Carlo simulations.
        """
        return sum(rand.sample(deck,n))
    
    @staticmethod
    def listn(deck,n=1):
        """
        Returns n-card list from a given deck WITHOUT UPDATING THE DECK. This is
        useful for Monte Carlo simulations.
        """
        return rand.sample(deck,n)