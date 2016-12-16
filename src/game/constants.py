import math

"""
	Options
"""

"""
	Choose terminal display
	0 for move trail; 1 for only current move; 2 for only final; -1 for nothing
	Do not choose 1 (current move) with mcts
"""
EVERY_MOVE = -1

# 1 for debug prints, 0 for no standard run
DEBUG = 0

# If false, uses iteration limit
USETIMELIMIT = False

# Computational budget in number of iterations
ITERATIONS = 50

# Computational budget in seconds (float)
TIMELIMIT = 0.1

# Exploration weighting
UCTCONSTANT = 8000 / math.sqrt(2)

# Weighting of heuristic in uct
HEURISTICCONSTANT = 0

# Weighting of empty tiles in heuristic
EMPTYCONSTANT = 5

HEIGHT = 4

WIDTH = 4

# Scoring scheme
# 0 -> Traditional 2048 scoring, merges result in score of new tile added
# 1 -> Score updated to the total sum of the tiles
# 2 -> Score updated to the total sum of the log_2 value of the tiles
SCORING = 0

"""
DO NOT MODIFY
"""
# Directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

QUIT = 5

# if USETIMELIMIT:
# 	print "Computational bound: " + str(TIMELIMIT) + " seconds"
# else:
# 	print "Computational bound: " + str(ITERATIONS) + " iterations"
# print "uct constant: " + str(UCTCONSTANT)
# print "total heuristic constant: " + str(HEURISTICCONSTANT)
# print "heuristic empty tile constant: " + str(EMPTYCONSTANT)