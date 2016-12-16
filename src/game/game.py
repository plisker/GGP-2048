"""
2048 game
"""
import random
import sys, tty, termios
import curses
import copy
import math
from constants import *

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


# Scoring scheme
# 0 -> Traditional 2048 scoring, merges result in score of new tile added
# 1 -> Score updated to the total sum of the tiles
# 2 -> Score updated to the total sum of the log_2 value of the tiles -- merges can lower total score!
# Create more in self.update_score function!

class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    def __init__(self, grid_height, grid_width, scoring=0):
        self._height = grid_height
        self._width = grid_width
        self._grid = []
        self._scoring = scoring
        self.reset()
        self._borders = {UP: [(0, col) for col in range(self._width)],
                   DOWN: [(self._height-1, col) for col in range(self._width)],
                   LEFT: [(row, 0)for row in range(self._height)],
                   RIGHT: [(row, self._width-1) for row in range(self._height)]}
        self._score = 0

        if EVERY_MOVE == 1:
            self.prepare_terminal_output()
        
        self.board_print()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for _ in range(self._width)]
                     for _ in range(self._height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        res = ""
        for index in range(len(self._grid)):
            res+=str(self._grid[index])+"\n"
        return res

    def prepare_terminal_output(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def cut(self, start, direction, steps):
        """
        makes a list and return it
        """
        res = []
        for step in range(steps):
            row = start[0] + step * direction[0]
            col = start[1] + step * direction[1]
            res.append(self._grid[row][col])
        return res

    def simulate_cut(self, start, direction, steps, grid):
        """
        makes a list and return it
        """
        res = []
        for step in range(steps):
            row = start[0] + step * direction[0]
            col = start[1] + step * direction[1]
            res.append(grid[row][col])
        return res   

    def merge(self, line):
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

    def modify(self, start, direction, steps, merged):
        """
        modifies the grid
        """
        for step in range(steps):
            row = start[0] + step * direction[0]
            col = start[1] + step * direction[1]
            self._grid[row][col] = merged[step]

    def simulate_modify(self, start, direction, steps, merged, grid):
        """
        modifies the grid
        """
        for step in range(steps):
            row = start[0] + step * direction[0]
            col = start[1] + step * direction[1]
            grid[row][col] = merged[step]

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
            cutted = self.cut(index, OFFSETS[direction], steps)
            merged, sum_score = self.merge(cutted)
            score = self.update_score(self._score, sum_score)
            self._score = score
            if cutted != merged:
                changed = True
            self.modify(index, OFFSETS[direction], steps, merged)
        if changed:
            self.new_tile()
            self.board_print()

    def get_successor(self, direction, grid, score):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        steps = self._height
        changed = False
        if direction == RIGHT or direction == LEFT:
            steps = self._width
        for index in self._borders[direction]:
            cutted = self.simulate_cut(index, OFFSETS[direction], steps, grid)
            merged, sum_score = self.merge(cutted)
            score = self.update_score(score, sum_score)
            if cutted != merged:
                changed = True
            self.simulate_modify(index, OFFSETS[direction], steps, merged, grid)
            
            # self.alert("Move completed.")
        
        if changed:
            # self.alert("The board changed!")

            self.simulate_new_tile(grid)

            # self.alert("A new tile was added.")

        else:
            # self.alert("The board did not change.")
            # print "BOARD DID NOT CHANGE"
            grid = None

        return grid, score

    def get_state(self):
        return self._grid

    def get_score(self):
        return self._score

    # Useful in case we change how tiles are stored in memory, whether as true value or log_2(tile)
    # TODO: whenever tile value is accessed, use this function
    def get_tile_value(self, tile):
        return tile

    def update_score(self, starting_score, added_score):
        new_score = starting_score
        if self._scoring == 0:
            new_score += added_score
        if self._scoring == 1:
            new_score = 0
            for row in self._grid:
                for tile in row:
                    new_score += self.get_tile_value(tile)        
        if self._scoring == 2:
            new_score = 0
            for row in self._grid:
                for tile in row:
                    tile_value = self.get_tile_value(tile)
                    if tile_value > 0:
                        new_score += int(math.log(tile_value, 2))
        return new_score

    def direction_quick(self, grid, direction):
        steps = self._height

        # Check if primary direction (i.e., the inputted direction) is a legal move
        primary_legal = False

        # Check if secondary direction (i.e., the opposite of inputted direction) is legal
        secondary_legal = False

        if direction == RIGHT or direction == LEFT:
            steps = self._width
        for index in self._borders[direction]:
            cutted = self.simulate_cut(index, OFFSETS[direction], steps, grid)
            
            if not primary_legal:
                for i in range(len(cutted)-1):
                    index = i+1
                    tile = cutted[index]
                    if tile == 0:
                        continue
                    else:
                        if cutted[index-1] in [0, tile]:
                            primary_legal = True
                            break

            if not secondary_legal:
                for i in range(len(cutted)-1):
                    index = len(cutted)-(i+2)
                    tile = cutted[index]
                    if tile == 0:
                        continue
                    else:
                        if cutted[index+1] in [0, tile]:
                            secondary_legal = True
                            break

            if primary_legal and secondary_legal:
                break

        if direction == 1:
            primary = 1
            secondary = 2
        elif direction == 2:
            primary = 2
            secondary = 1
        elif direction == 3:
            primary = 3
            secondary = 4
        else:
            secondary = 4
            primary = 3

        legal = []
        if primary_legal:
            legal.append(primary)
        if secondary_legal:
            legal.append(secondary)

        return legal


    # Can probably make more efficient by first checking for empty tiles...
    def legal_moves(self, grid):
        legal = []

        vertical = self.direction_quick(grid, UP)
        horizontal = self.direction_quick(grid, LEFT)
        legal = vertical + horizontal

        if legal == []:
            # self.alert("No more moves!")
            legal = None
        
        return legal

    def new_tile(self):
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

    def simulate_new_tile(self, grid):
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
            if grid[row][col] == 0 :
                flg = False
        if random.random() <= .1 :
            grid[row][col] = 4
        else:
            grid[row][col] = 2
    
    def board_print(self):
        if EVERY_MOVE == 0:
            self.simple_print()
            legal = self.legal_moves(self._grid)
            print "Possible legal moves:", self.legal_moves(self._grid)
            if not legal:
            	self.end_game()
        if EVERY_MOVE == 1:
            self.complex_print()
        if EVERY_MOVE == 2 or EVERY_MOVE == -1:
            pass

    def complex_print(self):
        self.stdscr.clear()
        table = self.pretty_grid_print()
        self.stdscr.addstr('\n'.join(table))
        self.stdscr.refresh()

    def simple_print(self):
        print "\nScore: "+str(self.update_score(self._score, 0))
        table = self.pretty_grid_print()
        print '\n'.join(table)

    def pretty_grid_print(self):
        s = [[str(e) for e in row] for row in self._grid]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        return table

    def end_game(self):
        if EVERY_MOVE != -1:
            if EVERY_MOVE == 1:
                curses.endwin()
            print "Game complete!"
            self.simple_print()
            print "Highest tile:", self.highest_tile()

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

    def alert(self, string):
        if EVERY_MOVE == 1:
            self.stdscr.addstr(string+"\n")
            self.stdscr.refresh()
        else:
            print string

    def highest_tile(self):
        highest = -1
        for row in self._grid:
            for element in row:
                if element > highest:
                    highest = element
        return highest