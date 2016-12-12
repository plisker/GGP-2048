import copy
import math
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


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
	def __init__(self, state, lastMove=None):
		
		self.state = state # game state
		
		self.value = 0 # sum of values of all the simulations played through this node
		
		self.numSimulations = 0 # number of simulations played through this node

		self.expandedChildren = [] # children of this node that have been expanded, type: Tree list

		self.lastMove = lastMove # move that got us to this state

		self.expanded = True


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
		Default simulation behavior. Typically random.
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
		bestVal = 0
		bestNode = None
		for child in self.expandedChildren:
			thisVal = child.getAvgValue()
			if (thisVal > bestVal) or (thisVal == bestVal and random.random() >= 0.5):
				bestNode = child
				bestVal = thisVal

		return bestNode.getLastMove() 


	"""
		methods used by the back propagation step
	"""
	def incNumSimulations(self):
		self.numSimulations += 1

	def addValue(value):
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
		return self.expanded


"""
	MCTS Tree with Upper Confidence Boudns for Trees (UCT) tree policy, 
	an expand all children expansion policy and random-move default 
	simulation policy
"""
class UctTree(Tree):
	
	def __init__(self,state,lastMove=None):
		Tree.__init__(self,state,lastMove)

	"""
		Upper Confidence Bound equation
		

					 	      sqrt(2 log(n_all))
	Value(state)		=	  	--------------
									n_state
	n_state is the number of simulations with moves including this node.
	n_all is total number of simulations

	if n_state = 0, this is understood to evaluate to infinity
	"""
	def upperConfidenceBound(self):
		if self.numSimulations == 0:
			return float("inf")
		else:
			return self.getAvgValue() + math.sqrt((2 * math.log(TOTALNUMSIMULATIONS))/self.numSimulations)

	"""
	UCT. Selects nodes with the highest UCB value, breaking ties randomly
	"""
	def select(self):
		currentNode = self; 
		bestUCB = self.upperConfidenceBound()
		path = [currentNode] 
		# counter = 1

		while (not currentNode.expandable()):
			# print("select run #" + str(counter) + "on node: " + str(currentNode))
			# counter += 1
			for child in currentNode.getExpandedChildren():
				thisUCB = child.upperConfidenceBound()
				if (thisUCB > bestUCB) or (thisUCB == bestUCB and random.random() >= 0.5):
					bestUCB = thisUCB
					currentNode = child

			path.append(currentNode)
		return (currentNode,path)

	"""
		Expands all children
	"""
	def expand(self):
		children = []
		for direction in [UP, DOWN, LEFT, RIGHT]:
			stateCopy = copy.deepcopy(self.state)
			newGrid,score = stateCopy.get_successor(direction, stateCopy._grid, stateCopy.get_score())
			print "newGrid:" + str(newGrid)
			
			if newGrid != None:
				newState = stateCopy.__class__(stateCopy._height(),stateCopy._width())
				newState._grid = newGrid
				newState.score = score
				newNode = UctTree(newState, lastMove=direction)
				self.expandedChildren.append(newNode)

		self.expanded = False

	"""
		Simulates a randomly played game from self
	"""
	def simulate(self):
		randomMove = random.choice([UP, DOWN, LEFT, RIGHT])
		currentNode = self
		# print currentNode.state
		successor = currentNode.state.get_successor(randomMove, successor._grid, successor.getScore())

		# Go until game ends
		while successor != None:
			randomMove = random.choice([UP, DOWN, LEFT, RIGHT])
			currentNode = successor
			successor = successor.state.get_successor(randomMove, successor._grid, successor.getScore())

		return currentNode.state.getScore()










