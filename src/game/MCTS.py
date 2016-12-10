import copy
import math
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]


"""
Class for a game tree with the information necessary for MCTS at each node.
For now there is some hard coded 2048 information in it but not much.

input: a game-state `state` i.e. a 2048 board object
"""
class Tree:
	def __init__(self, state):
		
		# game state
		self.state = state

		# sum of values of all the simulations played through this node
		self.value = 0

		# number of simulations played through this node
		self.numSimulations = 0

		# children of this node that have been expanded, type: Tree list
		self.expandedChildren = []

		# keep track of which nodes of actions have been expanded
		self.actionTaken = {UP:False, DOWN:False, LEFT:False, RIGHT:False}

	""" 
		Default expansion behavior is to expand all child nodes. 
		This can be changed to expand 1-3 nodes to lessen computational load.
	""" 
	def expand(self):
		children = []
		for direction in DIRECTIONS:
			children.append(self.expandChild(direction))
		return children

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
		Returns successor state after making `move`, doesn't expand that node
	"""
	def getChild(self,move):
		newState = copy.deepcopy(self.state)
		return newState.get_successor(move)

	"""
		Expands tree to include successor state after making `move`
	"""
	def expandChild(self,move):
		if not self.actionTake[move]:
			newState = self.getChild(move)
			self.expandedChildren.append(newState)
			self.actionTaken[move] = True
			return newState

	def incNumSimulations(self):
		self.numSimulations += 1

	def addValue(value):
		self.value += value

	def getNumSimulations(self):
		return self.numSimulations

	def getAvgValue(self):
		if self.numSimulations == 0:
			return 0
		else: 
			return self.value / self.numSimulations

	def get_state(self):
		return self.state.get_state()

	def legal_moves(self):
		return self.state.legal_moves(self.get_state())


	def getExpandedChildren(self):
		return self.expandedChildren

"""
	Adds `score` to value of all nodes in `path`
"""
def backPropagate(self,score,path):
	for node in path:
		node.incNumSimulations()
		node.addValue(score)


"""
	MCTS Tree with UCT tree policy and random-move simulation policy
"""
class UctTree(Tree):
	def __init__(self,state):
		Tree.__init__(self,state)

	def upperConfidenceBound(self):
		if self.numSimulations == 0:
			return float("inf")
		else:
			return self.getAvgValue() + math.sqrt((2 * math.log(TOTALNUMSIMULATIONS))/self.numSimulations)

	def select(self):
		currentNode = self; 
		bestUCB = self.upperConfidenceBound()
		path = [currentNode] 
		
		counter = 1
		while (currentNode.getExpandedChildren() == []):
			print("select run #" + str(counter))
			counter += 1
			for child in currentNode.getExpandedChildren():

				thisUCB = child.upperConfidenceBound()
				if (thisUCB > bestUCB) or (thisUCB == bestUCB and random.random() >= 0.5):
					bestUCB = thisUCB
					currentNode = child

			path.append(currentNode)

		return (currentNode,path)

	def simulate(self):
		randomMove = random.choice(DIRECTIONS)

		currentNode = self
		successor = self.getChild(randomMove)

		# Go until game ends
		while successor != None:
			randomMove = random.choice(DIRECTIONS)
			currentNode = successor
			successor = successor.getChild(randomMove)

		return currentNode.state.getScore()










