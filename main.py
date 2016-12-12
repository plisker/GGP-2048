from game import TwentyFortyEight
import sys, termios, tty
import random
import time
import MCTS
import numpy as np
import copy

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
QUIT = 5

# Number of iterations of MCTS
ITERATIONS = 1

TOTALNUMSIMULATIONS = 0

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
            play.print_board(end_game=True)
            break
        if key == -1:
            continue
        else:
            play.move(key)

def random_play(height, width):
    play = TwentyFortyEight(height, width)  
    moves = play.legal_moves()
    while moves != None:
        action = random.choice(moves)
        play.move(action)
        moves = play.legal_moves()
    
    play.print_board(end_game=True)


def mcts_play (height, width):
    play = TwentyFortyEight(height,width)

    end = False

    while not end:
        moves = play.legal_moves(play)
        if moves == None:
            end = True
            play.alert("No moves left, end")
        else:
            root = MCTS.UctTree(play)
            TOTALNUMSIMULATIONS = 0
            for _ in range(ITERATIONS):
                simulationNode, path = root.select()
                children = simulationNode.expand()
                print("children = " + str(children))
                for child,score in children:
                    print("child = " + str(child))
                    pathCopy = copy.deepcopy(path)
                    sim_score = child.simulate()
                    child.backPropagate(sim_score, pathCopy.append(child))
                TOTALNUMSIMULATIONS += 1  
            action = root.getBestAction() # TODO: define this method 
            play.move(action)
            play.alert("Move executed! Rinse and repeat.")


def corner_play(height, width):
    play = TwentyFortyEight(height, width)

    end = False

    while not end:
        # time.sleep(1)  
        moves = play.legal_moves()
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
            play.alert("Move executed! Rinse and repeat.")

    final_score = play.get_score()
    highest = play.highest_tile()
    play.print_board(end_game=True)
    return final_score, highest

def loop(n):
    scores = []
    highest = []
    try:
        for i in range(0,n):
            if i%100 == 0:
                print str(i)+" out of "+str(n)
            score, high = corner_play(4, 4)
            scores.append(score)
            highest.append(high)
    except:
        print "Some error occurred!"
    
    scores = np.array(scores)
    print "Mean of scores:", scores.mean()
    print "Max tile of all games:", max(highest) 


def main():
	# play_terminal(4, 4)
    random_play(4,4)
    # corner_play(4,4)
    # mcts_play(2,2)
	# loop(1000)

if __name__=='__main__':
        main()


