"""
2048 game
"""
import random
import sys, tty, termios
import curses
import copy

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
QUIT = 5

# Offsets for computing tile indices in each direction, DO NOT MODIFY
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

# 0 for move trail; 1 for only current move; -1 for nothing
PRINT_OPTION = 0


class TwentyFortyEight:
    """
    Class to run the logic for a classic 2048 game. 
    """
    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        self._grid = [[0 for _ in range(self._width)]
            for _ in range(self._height)]
        self._new_tile()
        self._new_tile()
        self._borders = {UP: [(0, col) for col in range(self._width)],
                   DOWN: [(self._height-1, col) for col in range(self._width)],
                   LEFT: [(row, 0)for row in range(self._height)],
                   RIGHT: [(row, self._width-1) for row in range(self._height)]}
        self.score = 0 
        self.print_board()


    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        res = ""
        for index in range(len(self._grid)):
            res+=str(self._grid[index])+"\n"
        return res

    def __eq__(self,other):
        return ((isinstance(other, self.__class__)) and (self._grid == other._grid) and (self.score))

    # def __deepcopy__(self,memo):
    #     new = TwentyFortyEight(self._height,self._width)
    #     new._board = self.get_board()
    #     new.score = self.get_score()
    #     return new

    """
    Public methods
    """
    def print_board(self, end_game=False):
        """
        Either prints each move alone (with the curses library), a trail of moves
        or nothing, if PRINT_OPTION is 1, 0 or -1
        """
        if PRINT_OPTION == 1:
            if end_game == True:
                curses.endwin()
                print "\nScore: "+str(self.score)
                for row in self._grid:
                    self._print_helper()
                print "Highest tile:", self.highest_tile()
            else:
                self.stdscr = curses.initscr()
                curses.noecho()
                curses.cbreak()
                self.stdscr.keypad(True)
                self.stdscr.clear()
                s = [[str(e) for e in row] for row in self._grid]
                lens = [max(map(len, col)) for col in zip(*s)]
                fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
                table = [fmt.format(*row) for row in s]
                self.stdscr.addstr('\n'.join(table))
                self.stdscr.refresh()

        elif PRINT_OPTION == 0:
            if end_game == True:
                print "Game complete!"    
            print "Highest tile:", self.highest_tile()
            self._print_helper()


    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        steps = self._height
        changed = False
        if direction == RIGHT or direction == LEFT:
            steps = self._width
        for index in self._borders[direction]:
            cutted = self._cut(index, OFFSETS[direction], steps)
            merged, sum_score = self._merge(cutted)
            self.score += sum_score
            if cutted != merged:
                changed = True
            self._modify(index, OFFSETS[direction], steps, merged)
        if changed:
            self._new_tile()
            self.print_board()

    def legal_moves(self):
        legal = []
        # Look at each square (i,j)
        for i in range(self._height):
            for j in range(self._width):

                # check for empty squares
                if self._grid[i][j] == 0:
                    if i != 0:
                        legal.append(RIGHT)
                    if i != self._height - 1:
                        legal.append(LEFT)
                    if j != 0:
                        legal.append(DOWN)
                    if j != self._width - 1:
                        legal.append(UP)

                # check if can move up
                if i != 0 and self._grid[i][j] == self._grid[i-1][j] and LEFT not in legal:
                    legal.append(LEFT)

                # check if can move left
                if j != 0 and self._grid[i][j] == self._grid[i][j-1] and UP not in legal:
                    legal.append(UP)

                # check if can move down
                if i != self._height - 1 and self._grid[i][j] == self._grid[i+1][j] and RIGHT not in legal:
                    legal.append(RIGHT)

                # check if can move right
                if j != self._width - 1 and self._grid[i][j] == self._grid[i][j+1] and DOWN not in legal:
                    legal.append(DOWN)

        if legal == []:
            legal = None

        return legal

    def highest_tile(self):
        highest = -1
        for row in self._grid:
            for element in row:
                if element > highest:
                    highest = element
        return highest

    def alert(self, string):
        if PRINT_OPTION == 1:
            self.stdscr.addstr(string+"\n")
            self.stdscr.refresh()
            print string

    def get_state(self):
        return self._grid

    def get_score(self):
        return copy.deepcopy(self.score)

    def get_board(self):
        return copy.deepcopy(self._grid)

    """
    Private methods
    """
    def _new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        flg = True
        col = 0
        row = 0
        while flg :
            col = random.randrange(self._width)
            row = random.randrange(self._height)
            if self._grid[row][col] == 0 :
                flg = False
        if random.random() <= .1 :
            self._grid[row][col] = 4
        else:
            self._grid[row][col] = 2

    def _cut(self, start, direction, steps):
        """
        makes a list and return it
        """
        res = []
        for step in range(steps):
            row = start[0] + step * direction[0]
            col = start[1] + step * direction[1]
            res.append(self._grid[row][col])
        return res

    def _merge(self, line):
        """
        Function that merges a single row or column in 2048.
        """
        score = 0
        result = []
        line_dimension = len(line)

        # Create new list with all nonzero numbers on the left, merging as necessary
        last_value = -1
        for i, value in enumerate(line):
            if value == 0:
                pass
            else:
                if value == last_value:
                    new_tile = value*2
                    result[len(result)-1] = new_tile
                    score += new_tile
                    last_value = -1
                else:
                    result.append(value)
                    last_value = value

        zeros = line_dimension-len(result)
        
        # Pad with zeros
        if zeros != 0:
            for _ in range(zeros):
                result.append(0)

        return result, score

    def _modify(self, start, direction, steps, merged):
        """
        modifies the grid
        """
        for step in range(steps):
            row = start[0] + step * direction[0]
            col = start[1] + step * direction[1]
            self._grid[row][col] = merged[step]

    def _print_helper(self):
        print "\nScore: "+str(self.score)
        for row in self._grid:
            print row
        s = [[str(e) for e in row] for row in self._grid]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print '\n'.join(table)    
