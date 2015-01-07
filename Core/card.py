class Card:
    """
    This class generates and displays cards.
    Cards are represented as 64-bit integers with a single set bit. The card is
    determined by where this bit is set from position 0 to 52. For example, the
    two of clubs has an index of 0, so it is represented as 1<<0 or 1. The ace
    of spades has an index of 51, so it is represented as 1<<51 or 2^51.
    Indexing is arranged so that there are 13 blocks of 4 nibbles. Thus, the
    52 positions look something like this:

    Pos:   52-------------------------------------------------------------1
    Suit:  ♠♥♦♣ ♠♥♦♣ ♠♥♦♣ ♠♥♦♣ ♠♥♦♣ ♠♥♦♣ ♠♥♦♣ ♠♥♦♣ ♠♥♦♣ ♠♥♦♣ ♠♥♦♣ ♠♥♦♣ ♠♥♦♣   
    Rank:  AAAA KKKK QQQQ JJJJ TTTT 9999 8888 7777 6666 5555 4444 3333 2222

    The most important advantage is that hands can be built by simply adding up
    cards, since they are simply ints. This representation also makes it faster
    to evaluate 7-card hands.

    Inspired by subskybox's "A Poker hand analyzer in JavaScript using bit &
    mathematical operations".
    """
    allcardstrs = [r+s for r in 'AKQJT98765432' for s in 'shdc']
    allcardints = list(map(lambda x: 1<<x, range(51,-1,-1)))
    
    STR2INT = dict(zip(allcardstrs,allcardints))

    INT2INDEX = dict(zip(allcardints,range(51,-1,-1)))
    
    INT2STR = dict(zip(allcardints,allcardstrs))

    DISPRANKS = ''.join(map(lambda x:x*4,'AKQJT98765432'))
    
    @staticmethod
    def str2int(cardstr):
        """
        Returns the integer representation of a card given its string such as
        Ah or 8c.
        """
        return Card.STR2INT[cardstr]

    @staticmethod
    def all2int(cardlist):
        """
        Returns the integer representation of a list of card strings as a single
        integer.
        """
        return sum(map(Card.str2int,cardlist))

    @staticmethod
    def int2str(cardint):
        """
        Returns the rank and suit string for given n-cards.
        """
        pret = []
        while cardint != 0:
            pret.append(Card.INT2STR[cardint & -cardint])
            cardint &= cardint-1
        return pret

    @staticmethod
    def int2index(cardint):
        """
        Returns the index from 0 to 51 of a given single card int.
        """
        return Card.INT2INDEX[cardint]
    
    @staticmethod
    def disp(hand):
        """
        Given an n-hand of cards, display the hand in its binary representation.
        """
        binstr = bin(hand).zfill(63)
        for i in range(52,0,-1):
            print(Card.DISPRANKS[-i] if binstr[-i]=='1' else '.',end='')
            print(' ' if i%4 == 1 else '',end='')
        print('')