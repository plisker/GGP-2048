import math

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# ?
QUIT = 5

# Choose Terminal Output
# 0 for move trail; 1 for only current move; 2 for only final; -1 for nothing
# Do not choose 1 (current move) with mcts
EVERY_MOVE = -1

# 1 for debug prints, 0 for no standard run
DEBUG = 0

# If false, uses iteration limit
USETIMELIMIT = False

# Computational budget in number of iterations
ITERATIONS = 5

# Computational budget in seconds (float)
TIMELIMIT = .01

# Exploration weighting
UCTCONSTANT = 8000 / math.sqrt(2)

# Weighting of heuristic in uct
HEURISTICCONSTANT = 300

# Weighting of empty tiles in heuristic
EMPTYCONSTANT = 5

if USETIMELIMIT:
	print "Computational bound: " + str(TIMELIMIT) + " seconds"
else:
	print "Computational bound: " + str(ITERATIONS) + " iterations"
print "uct constant: " + str(UCTCONSTANT)
print "total heuristic constant: " + str(HEURISTICCONSTANT)
print "heuristic empty tile constant: " + str(EMPTYCONSTANT)