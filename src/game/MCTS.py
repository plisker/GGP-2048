import copy
import math
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


"""
Class for a game tree with the information necessary for MCTS at each node.
For now there is some hard coded 2048 information in it but not much.

input: a game-state `state` i.e. a 2048 board object
"""
class Tree:
	def __init__(self, state, lastMove=None):
		
		self.state = state # game state
		
		self.value = 0 # sum of values of all the simulations played through this node
		
		self.numSimulations = 0 # number of simulations played through this node

		self.expandedChildren = [] # children of this node that have been expanded, type: Tree list

		self.lastMove = lastMove # needed for the evaluation step

		self.expanded = True

	""" 
		Default expansion behavior is to expand all child nodes. 
		This can be changed to expand 1-3 nodes to lessen computational load.

		Input: None
		Output: None
	""" 
	def expand(self):
		raise NotImplemented()

	"""
		Adds `score` to value of all nodes in `path`
	"""
	def backPropagate(self,score,path):
		for node in path:
			node.incNumSimulations()
			node.addValue(score)

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
		TreePolicy algorithm
	 	input: none
	 	output: (node,path) where `node` is node chosen to simulate from
	 			and `path` was the path used to get to `node`
	"""
	def select(self):
		raise NotImplemented()

	"""
		Default simulation behavior. Typically random.
		input: none
		output: score
	"""
	def simulate(self):
		raise NotImplemented()


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
		methods used by the ???
	"""
	def legal_moves(self):
		return self.state.legal_moves(self.get_state())

	def getAvgValue(self):
		if self.numSimulations == 0:
			return 0
		else: 
			return self.value / self.numSimulations

	def get_state(self):
		return self.state.get_state()


	def getExpandedChildren(self):
		return self.expandedChildren

	def getLastMove(self):
		return self.lastMove

	def expandable(self):
		return self.expanded


"""
	MCTS Tree with UCT tree policy and random-move simulation policy
"""
class UctTree(Tree):
	def __init__(self,state,lastMove=None):
		Tree.__init__(self,state,lastMove)

	def upperConfidenceBound(self):
		if self.numSimulations == 0:
			return float("inf")
		else:
			return self.getAvgValue() + math.sqrt((2 * math.log(TOTALNUMSIMULATIONS))/self.numSimulations)

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










