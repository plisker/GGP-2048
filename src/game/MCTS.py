import copy
import math
import random
import game
from constants import *

"""
	used by all 2048 trees to call get_successors
"""
game = game.TwentyFortyEight(4,4)

def zerolog(x):
	if x <= 0:
		return 0
	else:
		return math.log(x,2) 

def heuristic(grid):
	score = 0
	for corner in ["top-left","top-right","bottom-left","bottom-right"]:
		corner_score = 0
		for i in range(len(grid) - 1):
			for j in range(len(grid[0]) - 1):
				if grid[i][j] == 0:
					score += EMPTYCONSTANT
				if corner == "top-left":
					if grid[i][j] >= grid[i][j+1]:
						# score += 1
						# score += j
						score += zerolog(grid[i][j]) - zerolog(grid[i][j+1])
					if grid[i][j] >= grid[i+1][j]:
						# score += 1
						# score += j
						score += zerolog(grid[i][j]) - zerolog(grid[i+1][j])
				elif corner == "top-right":
					if grid[i][j] <= grid[i][j+1]:
						# score += 1
						# score += j
						score += zerolog(grid[i][j+1]) - zerolog(grid[i][j])
					if grid[i][j] >= grid[i+1][j]:
						# score += 1
						# score += j
						score += zerolog(grid[i][j]) - zerolog(grid[i+1][j])
				elif corner == "bottom-left":
					if grid[i][j] >= grid[i][j+1]:
						# score += 1
						# score += j
						score += zerolog(grid[i][j]) - zerolog(grid[i][j+1])
					if grid[i][j] <= grid[i+1][j]:
						# score += 1
						# score += j
						score += zerolog(grid[i+1][j]) - zerolog(grid[i][j])
				elif corner == "bottom-right":
					if grid[i][j] <= grid[i][j+1]:
						# score += 1
						# score += j
						score += zerolog(grid[i][j+1]) - zerolog(grid[i][j])
					if grid[i][j] <= grid[i+1][j]:
						# score += 1
						# score += j
						score += zerolog(grid[i+1][j]) - zerolog(grid[i][j])

		score = max([corner_score,score])

	score = score * HEURISTICCONSTANT
	# print "heuristic called: " + str(score)
	return score



"""
	Parent class for a game tree with the information necessary for MCTS
	at each node. Each child node is itself another Tree instance in the tree.
	The root node should be the only one with getLastMove = None.

	The methods `select`, `expand` and `simulate` are left
	should be defined in inheriting classes according to the tree policy,
	expansion policy, and default simulation policy you'd like.

	input: a game-state `state` i.e. a 2048 board object
"""
class Tree:
	def __init__(self, state, lastMove=None, score=0):
		
		self.state = state # game state
		
		self.score = 0 # score within game state

		self.value = 0 # sum of values of all the simulations played through this node
		
		self.numSimulations = 0 # number of simulations played through this node

		self.expandedChildren = [] # children of this node that have been expanded, type: Tree list

		self.lastMove = lastMove # move that got us to this state

		self.expanded = False

		actions_left = []
		for direction in [UP,DOWN,LEFT,RIGHT]:
			successor,_ = game.get_successor(direction, copy.deepcopy(self.state), 0)
			if successor != None:
				actions_left.append(direction)
		
		self.actions_left = actions_left

		# self.maxValue = 0 # attempted to use maximum simulation result as indicator of state value... didn't work well

	""" 
		Expansion policy. Typically simply either one or all nodes are expanded,
		depending on computational resources.
		
		Input: None
		Output: None
	""" 
	def expand(self):
		raise NotImplemented()


	""" 
		Tree policy algorithm i.e. Upper Confidence Bound for Trees (UCT)
	 	input: none
	 	output: (node,path) where `node` is node chosen to simulate from
	 			and `path` was the path used to get to `node`
	"""
	def select(self):
		raise NotImplemented()

	"""
		'Rollout policy' i.e. default simulation behavior. Typically random.
		input: None
		output: score
	"""
	def simulate(self):
		raise NotImplemented()


	"""
		Adds `score` to value of all nodes in `path`
	"""
	def backPropagate(self,score,path):
		for node in path:
			node.incNumSimulations()
			node.addValue(score)

	"""
		Returns the best move, the move that leads to the child state with
		the highest average value.
	"""
	def evaluate(self):
		bestVal = -1
		bestNode = None
		for child in self.expandedChildren:
			thisVal = child.getValue() # max child
			# thisVal = child.numSimulations # most robust child
			if (thisVal > bestVal) or (thisVal == bestVal and random.random() >= 0.5):
				bestNode = child
				bestVal = thisVal

		if bestNode == None:
			# print "random move"
			return random.choice([UP, DOWN, LEFT, RIGHT])
		else:
			# moves = ["up", "down","left","right"]
			bestMove = bestNode.getLastMove() 
			# print "non random move: " + str(moves[bestMove - 1])
			return bestMove


	"""
		methods used by the back propagation step
	"""
	def incNumSimulations(self):
		self.numSimulations += 1

	def addValue(self,value):
		self.value += value
		# if value > self.maxValue:
		# 	self.maxValue = value

	def getNumSimulations(self):
		return self.numSimulations

	"""
		Output: average value of the node per simulation. 
		Called by select() and evaluate()
	"""
	def getValue(self):
		return self.getAvgValue()

	"""
		Default node value: average simulation value
	"""
	def getAvgValue(self):
		if self.numSimulations == 0:
			return 0
		else: 
			return self.value / self.numSimulations

	"""
		Called by evaluate()
	"""
	def getLastMove(self):
		return self.lastMove

	"""
		Called by select()
	"""
	def getExpandedChildren(self):
		return self.expandedChildren

	def expandable(self):
		return (not (self.actions_left == []))



"""
	MCTS Tree with Upper Confidence Boudns for Trees (UCT) tree policy, 
	an expand all children expansion policy and random-move default 
	simulation policy
"""
class UctTree(Tree):
	
	def __init__(self,state,lastMove=None,score=0):
		Tree.__init__(self,state,lastMove,score)
		self.heuristic_value = heuristic(state)
		
	"""""""""""""""

	Public methods

	"""""""""""""""
	
	def select(self):
		return self.uct()

	
	def expand(self):
		self.expand_one_random()
		# self.expand_all()

	def simulate(self):
		# return self.simulate_score()
		# return self.simulate_highest_tile()
		return self.simulate_heuristic()

	
	"""""""""""""""

	Private methods

	"""""""""""""""

	"""
		UCT. Selects nodes with the highest UCB value, breaking ties randomly
	"""
	def uct(self):
		# initialized search at root (this method is meant for the root node), thus self is the root
		current_node = self
		path = [current_node]
	
		# We want to select the first node we in encounter that we can expand
		while (not current_node.expandable()):
		
			# Get children of current_node so we can choose among them
			children = current_node.getExpandedChildren()
		
			# choose to descend unto the child with highest UCB, break ties by chance	
			maxUCB = -1
			for child in children:
				thisUCB = child.upperConfidenceBound(current_node.getNumSimulations())
				if thisUCB > maxUCB:
					current_node = child
					children = grandchildren
					maxUCB = thisUCB

			# append each chosen node to path
			path = path + [current_node]

		return current_node, path

	def expand_one_random(self):
		# choose a random available action 
		random_action = random.choice(self.actions_left)
		
		# generate successor grid from random action
		newGrid,newScore = game.get_successor(random_action, copy.deepcopy(self.state), self.score)
		
		if newGrid == None:
			raise Exception("hmm")
		else:
			newNode = UctTree(newGrid, lastMove=random_action, score=newScore)
			self.expandedChildren.append(newNode)

	# def expand_one_heuristic(self):
	# 	# choose a random available action 
	# 	random_action = random.choice(self.actions_left)
		
	# 	newGrid,newScore = game.get_successor(random_action, copy.deepcopy(self.state), self.score)
		
	# 	if newGrid == None:
	# 		raise Exception("hmm")
	# 	else:
	# 		newNode = UctTree(newGrid, lastMove=random_action, score=newScore)
	# 		self.expandedChildren.append(newNode)

	"""
		Expands all children
	"""
	def expand_all(self):
		children = []
		for direction in [UP, DOWN, LEFT, RIGHT]:
			newGrid,score = game.get_successor(direction, copy.deepcopy(self.state), self.score)
			if newGrid != None:
				newNode = UctTree(newGrid, lastMove=direction, score=score)
				self.expandedChildren.append(newNode)

		self.expanded = True


	"""
		Upper Confidence Bound equation
		

					   _ 	     2 * k * sqrt(2 * ln(n_p))
		UCB(s)  	=  V(s)	+  ----------------------------
										   n_s
		_
		V(s) = average value of the child node in simulation
		n_p is the number of simulations done from the parent node
		n_s is the number of simulations done from the child node
		k is a constant, to be tuned

		Note: if n_s= 0, Value(state) is understood to evaluate to infinity
	"""
	def upperConfidenceBound(self,n_p):
		k = UCTCONSTANT
		n_s = self.numSimulations
		h = self.heuristic_value

		if self.numSimulations == 0:
			return float("inf")
		else:
			return self.getValue() + (2 * k * math.sqrt((2 * math.log(n_p))/n_s)) + (h / (n_s + 1))

	"""
		Simulates a randomly played game from self & returns the final score
	"""
	def simulate_score(self):
		randomMove = random.choice([UP, DOWN, LEFT, RIGHT])
		currentNodeState = copy.deepcopy(self.state)
		currentNodeScore = copy.deepcopy(self.score)
		successor,successorScore = game.get_successor(randomMove, currentNodeState, currentNodeScore)
		while (successor != None):
			currentNodeState = successor
			currentNodeScore = successorScore
			randomMove = random.choice([UP, DOWN, LEFT, RIGHT])
			successor,successorScore = game.get_successor(randomMove, currentNodeState, successorScore)
			
		return currentNodeScore

	"""
		Simulates a randomly played game from self & returns the highest tile
	"""
	def simulate_highest_tile(self):
		
		randomMove = random.choice([UP, DOWN, LEFT, RIGHT])
		currentNodeState = copy.deepcopy(self.state)
		currentNodeScore = self.highest_tile(currentNodeState)
		successor,_ = game.get_successor(randomMove, currentNodeState, currentNodeScore)
		successorScore = self.highest_tile(successor)

		while successor != None:
			successorScore = self.highest_tile(successor)
			currentNodeState = successor
			currentNodeScore = successorScore
			randomMove = random.choice([UP, DOWN, LEFT, RIGHT])
			successor, _ = game.get_successor(randomMove, currentNodeState, successorScore)
			
		return currentNodeScore
	"""
	
	TODO: Simulates a game played using heuristics & returns final score 
	"""
	def simulate_heuristic(self):
		best_successor = copy.deepcopy(self.state)
		best_score = 0

		while (best_successor != None):
			
			current_state = best_successor	
			best_score = -1
			best_move = None
			best_successor = None
			
			for direction in [UP, DOWN, LEFT, RIGHT]:
				current_state_copy = copy.deepcopy(current_state)
				successor,_ = game.get_successor(direction, current_state_copy, 0)	
				if successor != None:
					successor_score = heuristic(successor)
					if successor_score > best_score:
						best_score = successor_score
						best_move = direction
						best_successor = successor

		return best_score


	def highest_tile(self,grid):
	    if grid == None:
	    	return 0
	    else:
		    highest = -1
		    for row in grid:
		        for element in row:
		            if element > highest:
		                highest = element
		    return highest

	"""
		Secure-child evaluation
		Returns the move that leads to the child state with the highest UCB
	"""
	def evaluate_secure(self):
		bestVal = -1
		bestNode = None
		for child in self.expandedChildren:
			thisVal = child.upperConfidenceBound(self.getNumSimulations()) # secure child
			# thisVal = child.numSimulations # most robust child
			if (thisVal > bestVal) or (thisVal == bestVal and random.random() >= 0.5):
				bestNode = child
				bestVal = thisVal

		if bestNode == None:
			# print "random move"
			return random.choice([UP, DOWN, LEFT, RIGHT])
		else:
			# moves = ["up", "down","left","right"]
			bestMove = bestNode.getLastMove() 
			# print "non random move: " + str(moves[bestMove - 1])
			return bestMove


	# def evaluate(self):
	# 	self.evaluate_secure()

	"""
		max value as value
	"""
	# def getValue(self):
	# 	return self.maxValue









