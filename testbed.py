from Core.card import Card
from Core.deck import Deck
from Core.eva import Eva
from Bot.sim import Sim
from Bot.player import *
from Bot.game import Game

# For testing purposes
import time
import cProfile



def accuracy_test():
    d = Deck.new()
    for i in range(200000):
       hand7 = Deck.pickn(d,7)
       val = Eva.eval7(hand7)
       if val>>60 == 8:
           print('DISPLAYING: '+str(hand7))
           Eva.pretty(val)
           Card.disp(hand7)
           print('Kicker cards: (Suitless)')
           Card.disp(val & 0xFFFFFFFFFFFFF)
           print('')

def speed_test():
    d = Deck.new()
    n = int(500000)
    print('Generating '+str(n)+' hands...',end=' ')
    hand7 = [Deck.pickn(d,7) for i in range(n)]
    print('Done')
    print('Evaluating '+str(n)+' hands...',end=' ')
    t = time.time()
    list(map(Eva.eval7,hand7))
    elap = time.time() - t
    print('Done')
    perf = n/elap # Checks per second
    print(str(perf/1e3)+' thousand checks per second.')
    print('')
    print('Pynapple is:')
    print(str(perf/51.52978)+' times faster than Pokerhand-eval')
    print(str(perf/15220.97)+' times faster than Deuces (MIT)')
    print(str(perf/142698.8)+' times faster than SpecialKEval')
    # On my computer, I'm getting:
    # Generating 500000 hands... Done
    # Evaluating 500000 hands... Done
    # 151.18506587247754 thousand checks per second.
    # 
    # Pynapple is:
    # 2933.935791545734 times faster than Pokerhand-eval
    # 9.932682731289631 times faster than Deuces (MIT)
    # 1.0594697774086226 times faster than SpecialKEval  

def time_test(n): # Then run cProfile.run('time_test(100000)',sort=2)
    d = Deck.new()
    for i in range(int(n)):
        Eva.eval7(Deck.pickn(d,7))

def monte_test():
    # Start a new game with 4 villains
    g = Game(4)
    # Deal an Ace pair to Hero (Player ID is -1)
    g.dealplayer(-1,Card.all2int(['As','Ah']))
    # Run a Monte-Carlo Simulation to check the odds of winning
    s = Sim(g,50000) # Default iters = 50000 which is about +/- 0.2% of true value
    print('Probability of hero winning: '+str(s.p_hero))
    print('Probability of villains winning: '+str(s.p_vils))
    # Deal the Flop
    g.dealcomm(Card.all2int(['Ks','Qc','Ad']),3)
    # Run another Simulation
    s = Sim(g,50000)
    print('Probability of hero winning: '+str(s.p_hero))
    print('Probability of villains winning: '+str(s.p_vils))


# monte_test()
cProfile.run('time_test(100000)',sort=2)
