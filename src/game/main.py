from game import TwentyFortyEight
import sys, termios, tty
import random
import time
import MCTS
import numpy as np
import copy
import math
import csv
import datetime
import getopt
from constants import *

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

def play_terminal(height, width, scoring):
    play = TwentyFortyEight(height, width, scoring)

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

def random_play(height, width, scoring):
    play = TwentyFortyEight(height, width, scoring)

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
    root = MCTS.UctTree(game.get_state())

    # (2) Repeatedly expand and search state tree based on samples. Repeat while
    # within our computational budget (iterations)
    start = time.clock()
    
    if USETIMELIMIT:
        ctr = 0
        while ((time.clock() - start) < TIMELIMIT):
            mcts_helper(root,ctr)
            ctr += 1
    else:
        for ctr in range(ITERATIONS):
            mcts_helper(root,ctr)   

    # (3) After compuational budget exceeded, halt planning and conduct the action
    #     leading to the node with the highest value
    return root.evaluate()

def mcts_helper(root,ctr):
    debug_print(" ")
    debug_print("-------------------------------------------")
    debug_print("Iteration " + str(ctr+1) + " of " + str(ITERATIONS))
    
    # (A) use tree policy to select most urgent expandable node
    simulationNode, path = root.select()
    
    if DEBUG == 1:
        for j,node in enumerate(path):
            debug_print("select chose" + str(node) + "at level " + str(j+1))

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


"""
    Repeatedly calls UCT implementation to determine each move
"""
def mcts_play(height, width, scoring):
    # debug_print("playing with " + str(ITERATIONS) + " iterations", force=True)
    
    # Start a new game
    play = TwentyFortyEight(height, width, scoring)

    
    
    # Play until end of game
    counter = 1 
    while True:
        
        # Stop if end of game
        grid = copy.deepcopy(play.get_state()) 
        moves = play.legal_moves(grid)
        if moves == None:
            break
    
        debug_print("*******************************\n"+ "Move #" + str(counter))

        # choose next action using mcts
        action = mcts(play)
        
        # execute chosen action
        play.move(action)

        counter += 1
        debug_print(" ")

    # Game's over dude
    final_score = play.get_score()
    highest = play.highest_tile()
    play.end_game()
    return final_score, highest

def corner_play(height, width, scoring):
    play = TwentyFortyEight(height, width, scoring)

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

def loop(height, width, strategy,scoring, n):
    scores = []
    highest = []
    for i in range(0,n):
        if i >= 50 and i % 10 == 0:
                print "Test " + str(i+1)+ " out of " + str(n)
        score, high = strategy(height, width, scoring)
        
        print "score:" + str(score)
        print "high tile:" + str(high)

        scores.append(score)
        highest.append(high)

    
    scores = np.array(scores)
    if highest != []:
        print "Mean of scores:", scores.mean()
        print "Max tile of all games:", max(highest) 
    else:
        raise Exception("No games were played.")

"""
    Tests several * square * grid sizes n_each times each
"""
def size_test(size_min, size_max, scoring, n_each):
    for i in range(size_min,size_max):
        print "----------------------------------------------"
        print "Testing " + str(i) + " x " + str(i) + " grids:"
        loop(i, i, scoring, n_each)

def usage():
    print "usage: python main.py strategy repititions"
    print "valid strategies: \"mcts\", \"corner\", \"random\", \"terminal\", \"simple\""

def experiment1(filename, num_trials):
    scores = []
    highest = []
    fullfilename = filename + " " + str(datetime.datetime.now()) + ".csv"
    print "Experiment to file: " + fullfilename
    
    # run experiment
    for i in range(0,num_trials):
        
        print "Trial " + str(i+1)+ " of " + str(num_trials)
        
        start = time.clock()
        score, high = mcts_play(HEIGHT, WIDTH, SCORING)
        end = time.clock()
        
        print "Score: " + str(score)
        print "High tile: " + str(high)
        print "Duration: " + str(end - start) + "s"

        scores.append(score)
        highest.append(high)

    if highest == []:
        raise Exception("No games were played.")
 
    # summarize results in terminal
    scores_array = np.array(scores)
    average_score = str(scores_array.mean())
    highest_tile = str(max(highest))
  
    print "Average score: " + average_score
    print "Highest tile: " + highest_tile + "\n" 

    # write results to outfile
    with open(fullfilename, "ab") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["scores","high tiles"])
        for i,score in enumerate(scores):
            writer.writerow([score,highest[i]]) 
        writer.writerow(["average score", "highest tile"])
        writer.writerow([average_score, highest_tile])
    
def usage():
    print 'usage: main.py -n <num_trials> -f <outfile> -'

def main(argv):
    filename = None
    num_trials = None
    try:
        opts, args = getopt.getopt(argv,"n:f:")
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit(3)
        elif opt == "-n":
            num_trials = int(arg)
        elif opt == "-f":
            filename = arg
        else:
            usage()
            sys.exit(4)
    experiment1(filename,num_trials)

if __name__=='__main__':
    main(sys.argv[1:])



