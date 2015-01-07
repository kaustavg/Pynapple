""" WORK IN PROGRESS. TBD:
--> Rigorous testing.
"""

class Eva:
    """
    This class contains the meat of the whole thing: the bitwise evaluator for
    7-card hands.
    Evaluations are done using bit twiddling techniques for speed.
    This is a work in progress. For detailed explanation of how the evaluations
    are done, contact me (Kaustav).
    """

    ## Static constants (what is the equivalent to #define in Python?)
    COM0 = 0x1111111111111 # Binary comb of 0001 0001 0001 etc.
    COM1 = COM0 << 1
    COM2 = COM0 << 2
    COM3 = COM0 << 3

    # Straight
    STR = 0x11111 # 0001 0001 0001 0001 0001
    ACESTR = 0x1000000001111 # Ace high straight

    # Dictionary to convert h back into a rank (1 is lowest)
    # Note: The hand rankings for Texas Hold'em are:
    STRINGLOOK = {8:'Straight-Flush',
                  7:'Quad',
                  6:'Full House',
                  5:'Flush',
                  4:'Straight',
                  3:'Trips',
                  2:'Two Pair',
                  1:'Pair',
                  0:'High Card'}
    HANDLOOK = {0:6,
                1:8,
                2:4,
                3:7,
                4:7,
                5:5,
                6:7,
                7:0,
                8:1,
                9:2,
                10:2,
                11:3,
                12:6,
                13:6}                

    @staticmethod
    def eval7(hand):
        """
        Returns the hand strength bin and the kicker for a given 7-card hand.
        This is done by converting the hand to cumulative form. In cumulative
        form, the int is divided into 13 nibbles. Each nibble represents a rank.
        The nibbles are filled according to how many cards of that rank is in
        the hand. For example, if the nibble is 0001, then there is one card of
        that rank in the hand. If the nibble is 0011, then there are two cards
        of that rank in the hand etc.
        In general, if there are n cards of that rank in the hand, the nibble
        will take the value of (2^n) - 1. 
        In other words, the NUMBER OF BITS SET in each nibble determines how 
        many cards of that rank are in the hand.

        eval7 returns val variable, which represents the strength of the hand.
        BBB HHHH HHHH KKKK KKKK KKKK KKKK KKKK KKKK KKKK etc.
        hbin    highbit2 
           highbit1     top5 -->

        One of the most important tricks in this evaluator is the statement:
        h = cum%15
        This statement adds up each of the nibbles in the 64-bit integer which
        allows us to simultaneously check for Pairs, Two Pairs, Trips, Full
        Houses, and Quads.
        For 7 card evaluations, cum%15 returns:
            High card returns   7*1 = 7
            Pair returns        3+(5*1) = 8
            Two pair returns    3+3+(3*1) = 9 or 3+3+3+1 = 10
            Trips returns       7+(4*1) = 11
            Full House returns  7+3+(2*1) = 12 or 7+7+1 = 0 or 7+3+3 = 13
            Quads returns       15+(3*1) = 3 or 15+3+1 = 4 or 15+7 = 7* (-> 6)
        Note that getting a 7 could mean either quads+trips or high card.
        We can deal with that by checking cum & COM3 then
            High card returns 0
            Quad+trip returns nonzero (then make h = 6)

        Thus, the following spots are taken for h: (See HANDLOOK)
            0: Full House
            1: (Nothing)
            2: (Nothing)
            3: Quad
            4: Quad
            5: (Nothing)
            6: Quad
            7: High
            8: Pair
            9: Two Pair
           10: Two Pair
           11: Trips
           12: Full House
           13: Full House
        

        PROGRAM LAYOUT (Preliminary):
            Initialize variables
                mask = 0xFFFFFFFFFFFFF

            Convert to cumulative form

            Check for rank conbinations and correct for quads and trips (rare!)

            Lookup hbin

            If High Card, Pair, Two Pair, or Trip:
                Check for Flush
                    Check for flush of clubs
                        Set mask as clu
                    Check for flush of diamonds
                        Set mask as dia
                    Check for flush of hearts
                        Set mask as hea
                    Check for flush of spades
                        Set mask as spa
                        
            If High Card, Pair, Two Pair, Trip, or Flush
                Perform cum AND mask
                Check for Straight
                    Remove trailing zeros
                    Check for low-high straight
                        If already flush, make straight flush
                        Keep only 5 cards
                    Zero the lsb and remove trailing zeros
                    Check for med-high straight
                        If already flush, make straight flush
                        Keep only 5 cards
                    Zero the lsb and remove trailing zeros
                    Check for high-high straight
                        If already flush, make straight flush
                        Keep only 5 cards

            Determine highbit1
            Determine highbit2

            Compute top5
                if straight, straight-flush, or flush, it's just cum
                if pair
                    AND mask cum with not 0xF << highbit1*4
                    delete lsb
                    top5 is cum
                elif two pair
                    AND mask cum with not 0xF << highbit1*4
                    AND mask cum with not 0xF << highbit2*4
                    delete bottom two lsbs (slightly different from cumshift2)
                elif trips
                    AND mask cum with not 0xF << highbit1*4
                    delete bottom two lsbs (slightly different from cumshift2)
                elif fullhouse
                    top5 is 0
                elif quads
                    AND mask cum with not 0xF << highbit1*4
                    delete bottom two lsbs (slightly different from cumshift2)

            Shift hbin, highbit1, highbit2, top5 and return val 
                    
        """
        # Initialize Variables
        mask = 0xFFFFFFFFFFFFF
        highbit1 = 0
        highbit2 = 0
        top5 = 0

        # Convert to cumulative form
        clu = (hand & Eva.COM0) # Contains a 1 in every rank nibble with a club
        dia = (hand & Eva.COM1)>>1 # ... with a diamond
        hea = (hand & Eva.COM2)>>2 # ... with a heart
        spa = (hand & Eva.COM3)>>3 # ... with a spade

        cum = clu
        cum |= cum + dia
        cum |= cum + hea
        cum |= cum + spa

        # Check for rank combinations and correct for quads+trips
        h = cum%15
        h = 6 if (h == 7) and (cum & Eva.COM3 != 0) else h

        # Lookup hbin
        hbin = Eva.HANDLOOK[h]

        # Check for Flush...
        if hbin <= 3:
            # ...of clubs
            if clu%15 >= 5:
                hbin = 5
                mask = clu
            # ...of diamonds
            elif dia%15 >= 5:
                hbin = 5
                mask = dia
            # ...of hearts
            elif hea%15 >= 5:
                hbin = 5
                mask = hea
            # ...of spades
            elif spa%15 >= 5:
                hbin = 5
                mask = spa

        # Check for Straight
        if hbin <= 3 or hbin == 5:
            cum = cum & mask
            # Calculate cumshift1 and cumshift2
            cumshift1 = cum & (cum-1)
            cumshift2 = cumshift1 & (cumshift1-1)
            # Calculate lsb, lsbshift1, and lsbshift2
            lsb = cum&-cum
            lsbshift1 = cumshift1&-cumshift1
            lsbshift2 = cumshift2&-cumshift2
            # Check for high-high straight
            if (cumshift2//lsbshift2) & Eva.STR == Eva.STR:
                # If already flush, make straight-flush
                hbin = 8 if hbin == 5 else 4
                # Make cum keeping only 5 cards
                cum = cumshift2
                
            # Check for med-high straight
            elif (cumshift1//lsbshift1) & Eva.STR == Eva.STR:
                # If already flush, make straight-flush
                hbin = 8 if hbin == 5 else 4
                # Make cum keep only 5 cards
                cum = Eva.STR*lsbshift1
                
            # Check for low-high straight
            elif (cum//lsb) & Eva.STR == Eva.STR:
                # If already flush, make straight-flush
                hbin = 8 if hbin == 5 else 4
                # Make cum keep only 5 cards
                cum = Eva.STR*lsb
                
            # Check for Ace-low straight
            elif cum & Eva.ACESTR == Eva.ACESTR:
                # If already flush, make straight-flush
                hbin = 8 if hbin == 5 else 4
                # Make cum keep only 5 cards
                cum = Eva.ACESTR

        # Determine highbit1
        if hbin == 1 or hbin == 2:      # If Pair or Two Pair
            highbit1 = Eva.log2(cum & Eva.COM1)
        elif hbin == 3 or hbin == 6:    # If Trips or Full House
            highbit1 = Eva.log2(cum & Eva.COM2)
        elif hbin == 7:                 # If Quads
            highbit1 = Eva.log2(cum & Eva.COM3)

        # Determine highbit2
        if hbin == 2 or hbin == 6:      # If Two Pair or Full House
            # Mask highbit1 and find next highesest pair
            highmasked = cum & (~(15 << (highbit1 << 2)))
            highbit2 = Eva.log2(highmasked & Eva.COM1)

        # Determine top5
        if hbin == 1:
            # If Pair, mask highbit1 and delete bottom two LSBs
            top5 = cum & (~(3 << (highbit1 << 2)))
            top5 &= top5-1
            top5 &= top5-1
        elif hbin == 2:
            # If Two Pair, mask highbit1 and highbit2 and delete bottom two LSBs
            top5 = cum & (~(3 << (highbit1 << 2)))
            top5 &= ~(3 << (highbit2 << 2))
            top5 &= top5-1
            top5 &= top5-1
        elif hbin == 3:
            # If Trips, mask highbit1 and delete bottom two LSBs
            top5 = cum & (~(7 << (highbit1 << 2)))
            top5 &= top5-1
            top5 &= top5-1
        elif hbin == 6:
            # If Full House top5 is 0 (TBD: Can be optimized)
            top5 = 0
        elif hbin == 7:
            # If Quads, mask highbit1 and delete bottom two LSBs
            top5 = cum & (~(15 << (highbit1 << 2)))
            top5 &= top5-1
            top5 &= top5-1
        else:
            # If Straight, Flush, or Straight-Flush, it's already masked
            top5 = cum

        # Shift hbin and highbits
        hbin <<= 60
        highbit1 <<= 56
        highbit2 <<= 52

        # Return val
        return hbin | highbit1 | highbit2 | top5
            
                
    @staticmethod
    def log2(highbit):
        """
        Returns the index of the MSB // 4.
        """
        if   highbit & 0xF000000000000 > 0: # A nibble populated
            return 12
        elif highbit & 0xF00000000000 > 0: # K nibble populated
            return 11
        elif highbit & 0xF0000000000 > 0: # Q nibble populated
            return 10
        elif highbit & 0xF000000000 > 0: # J nibble populated
            return 9
        elif highbit & 0xF00000000 > 0: # T nibble populated
            return 8
        elif highbit & 0xF0000000 > 0: # 9 nibble populated
            return 7
        elif highbit & 0xF000000 > 0: # 8 nibble populated
            return 6
        elif highbit & 0xF00000 > 0: # 7 nibble populated
            return 5
        elif highbit & 0xF0000 > 0: # 6 nibble populated
            return 4
        elif highbit & 0xF000 > 0: # 5 nibble populated
            return 3
        elif highbit & 0xF00 > 0: # 4 nibble populated
            return 2
        elif highbit & 0xF0 > 0: # 3 nibble populated
            return 1
        else:
            return 0 # 2 nibble populated

    @staticmethod
    def pretty(val):
        """
        Prints a pretty string of the results of the evaluator.
        """
        hbin = val >> 60
        highbit1 = (val >> 56) & 15
        highbit2 = (val >> 52) & 15
        ranks = '23456789TJQKA'
        str1 = str(ranks[highbit1]) if highbit1>0 else ''
        str2 = (', '+str(ranks[highbit2])) if highbit2>0 else ''
        
        print((str1+str2+' '+Eva.STRINGLOOK[hbin]).strip())

    @staticmethod
    def val2binstr(val):
        """
        Prints the hand strength bin string from a given val.
        """
        print(Eva.STRINGLOOK[val>>60])
