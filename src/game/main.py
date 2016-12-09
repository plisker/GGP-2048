from game import TwentyFortyEight
import sys, termios, tty

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
    play = TwentyFortyEight(height, height)

    while True:
        key = get(play)
        if key == 5:
            play.end_game()
            break
        if key == -1:
            continue
        else:
            play.move(key)

def main():
    try:
        play_terminal(4, 4)
    except:
        print "Some error occurred!"

if __name__=='__main__':
        main()