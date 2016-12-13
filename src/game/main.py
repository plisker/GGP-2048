from game import TwentyFortyEight
import sys, termios, tty
import random
import time
import MCTS
import numpy as np
import copy
import math
import constants

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
QUIT = 5

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

def random_play(height, width):
    play = TwentyFortyEight(height, width)

    end = False

    counter = 1
    while not end:
        # time.sleep(1)
        print ("Move #" + str(counter))

        grid = play.get_state()    
        moves = play.legal_moves(grid)
        if moves == None:
            end = True
        else:
            action = random.choice(moves)
            play.move(action)
        counter += 1

    final_score = play.get_score()
    highest = play.highest_tile()
    play.end_game()
    return final_score, highest

def mcts(game):

    # create root node with start state
    root = MCTS.UctTree(game, game.get_state())

    # while within our computational budget (ITERATIONS)
    for i in range(constants.ITERATIONS):
        # print "Iteration " + str(i+1) + " of " + str(constants.ITERATIONS)
        
        # use tree policy to select most urgent expandable node
        simulationNode, path = root.select()

        # expand that node and retrieve its children
        simulationNode.expand()
        children = simulationNode.getExpandedChildren()
        
        # for each of the selected node's expanded children
        for child in children:
            
            # simulate a game till end
            score = child.simulate()
            
            # back-propagate the final score into the value of all nodes in 
            # the path to the selected node
            fullpath = path + [child]
            child.backPropagate(score, fullpath)

            constants.TOTALNUMSIMULATIONS += 1

    # return the direction of the child of root with the highest average value
    return root.evaluate()

def mcts_play (height, width):
    play = TwentyFortyEight(height, width)

    counter = 1

    # Play until end of game
    while True:
        
        print ("Move #" + str(counter))
        # check for end of game
        grid = play.get_state()
        moves = play.legal_moves(grid)
        if moves == None:
            break
        
        # select next action using mcts and execute
        action = mcts(play)
        play.move(action)
        counter += 1

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

def loop(n):
    scores = []
    highest = []
    try:
        for i in range(0,n):
            # if i%1 == 0:
            print str(i)+" out of "+str(n)
            # score, high = corner_play(4, 4)
            score, high = mcts_play(4,4)
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

def main():
    # corner_play(4,4)
    # random_play(4,4)
	# play_terminal(4, 4)
    mcts_play(4,4)
	# loop(10)

if __name__=='__main__':
        main()


