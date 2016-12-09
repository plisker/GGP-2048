import copy
import math
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

TOTALNUMSIMULATIONS = 0

class Node:
	def __init__(self, state, n):
		self.state = state
		self.n = n
		self.value = 0
		self.numSimulations = 0
		self.expandedChildren = []
		self.actionTaken = {UP:False, DOWN:False, LEFT:False, RIGHT:False}

	def expandChild(self,move):
		if not self.actionTake[move]:
			newstate = copy.deepcopy(self.state)
			newstate.move(move)
			self.expandedChildren.append(newstate)
			self.actionTaken[move] = True

	def expandAllChildren(self):
		children = []
		for direction in DIRECTIONS:
			self.expandChild(direction)

	def run (self):
		for i in range(self.n):
			result = self.select()
			score = self.simulate(result["nodeChoice"])
			TOTALNUMSIMULATIONS += 1
			self.backPropagate(score,result["path"])
		
		# return best initial action

	def backPropagate(self,score,path):
		for node in path:
			node.numSimulations += 1
			node.value += score

	def getNumSimulations(self):
		return self.numSimulations

	def getAvgValue(self):
		if self.numSimulations == 0:
			return None
		else: 
			return self.value / self.numSimulations

	def getExpandedChildren(self):
		return self.expandedChildren

	def select(self):
		raise NotImplemented()

	def simulate(self):
		raise NotImplemented()

class UBT_MCTS(Node):
	def __init__(self,MCST_Node,state):
		self = Node(state)

	def upperConfidenceBound(self):
		if self.numSimulations == 0:
			return float("inf")
		else:
			return self.getAvgValue() + math.sqrt((2 * math.log(TOTALNUMSIMULATIONS))/self.numSimulations)

	# UBT policy
	def select(self):
		
		currentNode = self
		path = [currentNode]

		while (currentNode.getExpandedChildren() != []):
			bestUCB = None; 
			bestChild = None; 
			for child in currentNode.expandedChildren:
				thisUCB = currentNode.upperConfidenceBound()
				
				if bestUCB == None:
					bestUCB = thisUCB
					bestChild = child
				elif (thisUCB == bestUCB and random.random() >= 0.5) or (thisUCB > bestUCB):
					bestUCB = thisUCB
					bestChild = child

			currentNode = bestChild
			path.append(currentNode)

		return {"nodeChoice":currentNode,"path":path}

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