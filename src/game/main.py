from game import TwentyFortyEight
import sys, termios, tty
import random
import time
import MCTS
import numpy as np
import copy
import math

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
QUIT = 5

DEBUG = 0

# Computational budget in number of iterations
ITERATIONS = 100

# Computational budget in seconds (float)
TIMELIMIT = 0.1

class _Getch:
    def __call__(self, play):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == 'q':
                pass
            else:
                if ch == '\x1b':
                    ch2 = sys.stdin.read(1)
                    ch = ch+ch2
                if ch == '\x1b[':
                    ch3 = sys.stdin.read(1)
                    ch = ch+ch3
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def get(play):
    inkey = _Getch()
    while(1):
        k = inkey(play)
        if k != '':
            break
    if k == '\x1b[A':
        return UP
    elif k == '\x1b[B':
        return DOWN
    elif k == '\x1b[C':
        return RIGHT
    elif k == '\x1b[D':
        return LEFT
    # Don't think this works!
    elif k == '\x1bO':
        play.stdscr.addstr("Not an valid move! Try again?\n")
        return -1
    elif k == 'A':
        return UP
    elif k == 'B':
        return DOWN
    elif k == 'C':
        return RIGHT
    elif k == 'D':
        return LEFT
    elif k == 'q':
        print "Quitting..."
        return QUIT
    else:
        play.stdscr.addstr("Not an arrow key! If you want to quit, press \'q\'\n") 
        play.stdscr.addstr("You pressed "+repr(str(k))+"\n") 
        play.stdscr.refresh()
        return -1

def play_terminal(height, width):
    play = TwentyFortyEight(height, width)

    while True:
        key = get(play)
        if key == 5:
            play.end_game()
            break
        if key == -1:
            continue
        else:
            play.move(key)

def debug_print(string, force=False):
    if DEBUG == 1 or force:
        print string

def random_play(height, width):
    play = TwentyFortyEight(height, width)

    end = False

    # counter = 1
    while not end:
        # time.sleep(1)
        # print ("Move #" + str(counter))

        grid = play.get_state()    
        moves = play.legal_moves(grid)
        if moves == None:
            end = True
        else:
            action = random.choice(moves)
            play.move(action)
        # counter += 1

    final_score = play.get_score()
    highest = play.highest_tile()
    play.end_game()
    return final_score, highest

"""
    Flat UCB
"""
def mcts_simple(game):
    root = MCTS.UctTree(game, game.get_state())

    # for _ in range(ITERATIONS):
    start = time.clock()
    while (time.clock() - start < TIMELIMIT):
        simulationNode, path = root.select()
        
        score = simulationNode.simulate()
        
        simulationNode.backPropagate(score, path)

    # return the direction of the child of root with the highest average value
    return root.evaluate()

"""
    High level of Upper Confidence Bound for Trees (UCT) planning for one move
"""
def mcts(game):
    
    # (1) create root node with start state
    root = MCTS.UctTree(game, game.get_state())

    # (2) Repeatedly expand and search state tree based on samples. Repeat while
    # within our computational budget (iterations) *[TODO: implement time based budget]
    # for i in range(ITERATIONS):
    start = time.clock()
    # if (time.clock() - start) < TIMELIMIT:
    #     print "yes"
    # else:
    #     print "no"
    ctr = 1
    while ((time.clock() - start) < TIMELIMIT):
        debug_print(" ")
        debug_print("-------------------------------------------")
        debug_print("Iteration " + str(ctr+1) + " of " + str(ITERATIONS))
        
        # (A) use tree policy to select most urgent expandable node
        simulationNode, path = root.select()
        
        if DEBUG == 1:
            for j,node in enumerate(path):
                debug_print("chose " + str(j) + ": " + str(node))

        debug_print ("simulation node: " + str(simulationNode) + " at depth " + str(len(path)))


        # (B) expand selected node and retrieve its children
        simulationNode.expand()
        children = simulationNode.getExpandedChildren()

        if children == []:
            debug_print("NO CHILDREN EXPANDED")
        debug_print("expanded nodes: " + str(children))

        # (C) Simulate a game for each of those children
        for j,child in enumerate(children):

            debug_print("simulating from " + str(j+1) + "th expanded node")
            
            # (i) Simulates game from child and retrieves final score
            score = child.simulate()

            debug_print("estimated score from " + str(j+1) + "th child:"+ str(score))
            
            fullpath = path + [child]

            debug_print("propagating score through path: " + str(fullpath))
            
            # (ii) back-propagate that final score into the value of all expanded nodes in the path to child
            child.backPropagate(score, fullpath)
        ctr += 1

    # (3) After compuational budget exceeded, halt planning and conduct the action
    #     leading to the node with the highest value
    return root.evaluate()

"""
    Repeatedly calls UCT implementation to determine each move
"""
def mcts_play (height, width):
    # debug_print("playing with " + str(ITERATIONS) + " iterations", force=True)
    
    # Start a new game
    play = TwentyFortyEight(height, width)

    counter = 1 
    
    # Play until end of game
    while True:
        
        # Stop if end of game
        grid = copy.deepcopy(play.get_state()) 
        moves = play.legal_moves(grid)
        if moves == None:
            break
    
        debug_print("*******************************")
        debug_print("*******************************")
        debug_print("Move #" + str(counter))
        
        # choose next action using mcts
        action = mcts(play)
        # action = mcts_simple(play)
        
        # execute chosen action
        play.move(action)

        counter += 1
        debug_print(" ")

    # Game's over dude
    final_score = play.get_score()
    highest = play.highest_tile()
    play.end_game()
    return final_score, highest

def corner_play(height, width):
    play = TwentyFortyEight(height, width)

    end = False

    while not end:
        # time.sleep(1)
        grid = play.get_state()    
        moves = play.legal_moves(grid)
        if moves == None:
            end = True
        else:
            if 1 in moves:
            	action = 1
            elif 3 in moves:
            	action = 3
            elif 4 in moves:
            	action = 4
            else:
            	action = 2
            play.move(action)

    final_score = play.get_score()
    highest = play.highest_tile()
    play.end_game()
    return final_score, highest

def loop(height,width,n):
    scores = []
    highest = []
    try:
        for i in range(0,n):
            # if i%1 == 0:
            print "Test " + str(i+1)+ " out of " + str(n)
            # score, high = corner_play(4, 4)
            score, high = mcts_play(height,width)
            # score, high = random_play(4,4)
            scores.append(score)
            highest.append(high)
    except:
        print "Some error occurred!"
    
    scores = np.array(scores)
    if highest != []:
        print "Mean of scores:", scores.mean()
        print "Max tile of all games:", max(highest) 
    else:
        raise Exception("No games were played.")

"""
    Tests several * square * grid sizes n_each times each
"""
def size_test(size_min,size_max,n_each):
    for i in range(size_min,size_max):
        print "----------------------------------------------"
        print "Testing " + str(i) + " x " + str(i) + " grids:"
        loop(i,i,n_each)

def main(strategy="mcts"):
    if strategy == "corner":
        corner_play(4,4)
    elif strategy == "random":
        random_play(4,4)
    elif strategy == "terminal":
	   play_terminal(4, 4)
    elif strategy == "simple":
        mcts_simple(4,4)
    elif strategy == "loop":
	   loop(4,4,30)
    elif strategy == "size":
        size_test(5,8,10)
    else:
        mcts_play(4,4)

if __name__=='__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()


