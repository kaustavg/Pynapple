from deck import Deck
from eva import Eva
from game import Game

"""
TBD: Make other math stuff (like equity)
"""

class Sim:
    """
    This holder class runs Monte Carlo Simulations for a given Game object,
    returning the probability of winning and other computations. The results of
    the simulation are stored in the Sim instance.
    Note that creating a Sim instance will automatically run the simulation!
    """
    def __init__(self,game,iters=50000): # Default iters will get +/- 0.1%
    	self.game = game
    	self.iters = iters
    	# Notation: 
    	# w_player represents 'Number of wins & ties for <player>'
    	# p_player represents 'Probability of <player> winning or tieing'

    	self.w_hero = 0
    	self.w_vils = [0]*self.game.n_vils

    	self.p_hero = self.w_hero/self.iters
    	self.p_vils = list(map(lambda x: x/self.iters,self.w_vils))

    	# Add variables for equity for each player (e_player?)

    	self.run()

    def run(self):
    	"""
    	Runs a Monte Carlo Simulation.
    	"""
    	# Figure out how many cards need to be randomly drawn
    	n_comm_todraw = 5 - self.game.n_comm
    	n_vils_todraw = self.game.n_vils * 2
    	n_todraw = n_comm_todraw + n_vils_todraw

    	# Shorter variable for the deck
    	d = self.game.deck

    	# List keeping track of wins & ties for all players
    	wins = [0]*(self.game.n_vils+1)

    	# Enter main loop
    	for i in range(self.iters):
    		picked = Deck.listn(d,n_todraw)
    		# Pull out the community cards
    		sim_comm = self.game.comm + sum(picked[:n_comm_todraw])
    		# Pull out the villain cards and add the hero hole
    		sim_holes = [picked[j]+picked[j+1] for j in range(n_comm_todraw,n_todraw-1,2)]
    		sim_holes.append(self.game.hero.hole)
    		# Create 7 card hands
    		sim_hands = map(lambda x: x+sim_comm,sim_holes)
    		# Determine vals
    		sim_vals = list(map(Eva.eval7,sim_hands))
    		# Determine winning val
    		sim_winningval = max(sim_vals)
    		for j in range(self.game.n_vils+1):
    			# Check if player won
    			if sim_vals[j] == sim_winningval:
    				# Increment win counter
    				wins[j] += 1

    	# Compute simulation results
    	self.w_hero = wins[-1]
    	self.w_vils = wins[:self.game.n_vils]

    	self.p_hero = self.w_hero/self.iters
    	self.p_vils = list(map(lambda x: x/self.iters,self.w_vils))
