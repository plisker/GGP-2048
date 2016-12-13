import copy
import math
import random
import constants

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# UCTCONSTANT = random.randint(2,10000)
# print "k = sqrt(" + str(UCTCONSTANT) + ")"
UCTCONSTANT = 5000 / math.sqrt(2)
# print "k = "  + str(UCTCONSTANT)
# print "robust child run"

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
	def __init__(self, game, state, lastMove=None):
		
		self.state = state # game state

		self.game = game
		
		self.value = 0 # sum of values of all the simulations played through this node
		
		self.numSimulations = 0 # number of simulations played through this node

		self.expandedChildren = [] # children of this node that have been expanded, type: Tree list

		self.lastMove = lastMove # move that got us to this state

		self.expanded = False

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
			thisVal = child.getAvgValue() # max child
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

	def getNumSimulations(self):
		return self.numSimulations

	"""
		Output: average value of the node per simulation. 
		Called by select() and evaluate()
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
		successors = []
		for direction in [UP,DOWN,LEFT,RIGHT]:
			successor,_ = self.game.get_successor(direction, copy.deepcopy(self.state), self.game.get_score())
			if successor != None:
				successors.append(successor)
		is_terminal = (successors == [])

		return (self.expanded and is_terminal)



"""
	MCTS Tree with Upper Confidence Boudns for Trees (UCT) tree policy, 
	an expand all children expansion policy and random-move default 
	simulation policy
"""
class UctTree(Tree):
	
	def __init__(self,game,state,lastMove=None):
		Tree.__init__(self,game,state,lastMove)

	"""
		Upper Confidence Bound equation
		

						 	     2 * k * sqrt(2 * ln(n_all))
		Value(state)		=	 ----------------------------
										   n_state
		n_state is the number of simulations with moves including this node.
		n_all is total number of simulations
		
		k is a constant, to be tuned

		if n_state = 0, Value(state) is understood to evaluate to infinity
	"""
	def upperConfidenceBound(self):
		k = UCTCONSTANT
		n_all = constants.TOTALNUMSIMULATIONS
		n_state = self.numSimulations

		if self.numSimulations == 0:
			return float("inf")
		else:
			return self.getAvgValue() + (2 * k * math.sqrt((2 * math.log(n_all))/n_state))

	"""
		UCT. Selects nodes with the highest UCB value, breaking ties randomly
	"""
	def select(self):
		# initialized search at root (this method is meant for the root node), thus self is the root
		current_node = self
		path = [current_node]
		
		# Get children of current_node so we can choose among them
		children = current_node.getExpandedChildren()
		
		# We want to select the first we in encounter in our search non-terminal node that we can expand
		while (children != []):
			# print "are children:" + str(children)
			# Get children of current_node so we can choose among them
			children = current_node.getExpandedChildren()
			# assert (children != []) # definitely gonna be triggered

			maxUCB = -1

			# choose to descend unto the child with highest UCB, break ties by chance
			for child in children:
				thisUCB = child.upperConfidenceBound()
				if thisUCB > maxUCB:
					current_node = child
					maxUCB = thisUCB
				elif thisUCB == maxUCB:
					current_node,maxUCB = random.choice([(current_node,maxUCB),(child,thisUCB)])

			# append each chosen node to path
			path = path + [current_node]

			# update children
			children = current_node.getExpandedChildren()

		# print "current depth: " + str(len(path))

		return current_node, path




		# currentNode = self
		# path = [self]
		# notExpandable = not currentNode.expandable()
		# notTerminal = True
		# # print currentNode.expandable()
		# while (notExpandable and notTerminal):
		# 	choices = currentNode.getExpandedChildren()
		# 	currentNode = choices[0]
		# 	maxUCB = currentNode.upperConfidenceBound()
		# 	for choice in choices:
		# 		if (not choice.expandable()):
		# 			thisUCB = choice.upperConfidenceBound()
		# 			if thisUCB > maxUCB:
		# 				currentNode = choice
		# 				maxUCB = thisUCB
		# 			elif thisUCB == maxUCB:
		# 				currentNode,maxUCB = random.choice([(currentNode,maxUCB),(choice,thisUCB)])

		# 	path.append(currentNode)

		# # print("We are " + str(len(path)) + " levels deep.")
		# return currentNode,path


	"""
		Expands all children
	"""
	def expand(self):
		# if self.expanded:
		# 	raise Exception("Error: Trying to expand already expanded node")

		children = []
		for direction in [UP, DOWN, LEFT, RIGHT]:
			newGrid,score = self.game.get_successor(direction, copy.deepcopy(self.state), self.game.get_score())
			
			if newGrid != None:
				newNode = UctTree(copy.deepcopy(self.game), newGrid, lastMove=direction)
				self.expandedChildren.append(newNode)

		self.expanded = True

	"""
		Simulates a randomly played game from self
	"""
	def simulate(self):
		
		randomMove = random.choice([UP, DOWN, LEFT, RIGHT])
		currentNodeState = copy.deepcopy(self.state)
		currentNodeScore = copy.deepcopy(self.game.get_score())
		successor,successorScore = self.game.get_successor(randomMove, currentNodeState, currentNodeScore)

		while successor != None:
			currentNodeState = successor
			currentNodeScore = successorScore
			randomMove = random.choice([UP, DOWN, LEFT, RIGHT])
			successor,successorScore = self.game.get_successor(randomMove, currentNodeState, successorScore)
			
		return currentNodeScore










