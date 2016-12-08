# this code works on the IDE of the course
#  http://www.codeskulptor.org/#user40_tB3zWKAKJL_4.py
"""
Clone of 2048 game.
"""
import random
import poc_2048_gui
import sys

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


# Progress bar with credit to http://stackoverflow.com/a/6169274 #



# def startProgress(self, title):
#     global progress_x
#     sys.stdout.write(title + ": [" + "-"*40 + "]" + chr(8)*41)
#     sys.stdout.flush()
#     progress_x = 0

# def progress(self, x):
#     global progress_x
#     x = int(x * 40 // 100)
#     sys.stdout.write("#" * (x - progress_x))
#     sys.stdout.flush()
#     progress_x = x

# def endProgress(self):
#     sys.stdout.write("#" * (40 - progress_x) + "]\n")
#     sys.stdout.flush()

        
def merge(line):
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


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        self._grid = []
        self.reset()
        self._borders = {UP: [(0, col) for col in range(self._width)],
                   DOWN: [(self._height-1, col) for col in range(self._width)],
                   LEFT: [(row, 0)for row in range(self._height)],
                   RIGHT: [(row, self._width-1) for row in range(self._height)]}
        self.score = 0

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

    def cut(self , start , direction , steps):
        """
        makes a list and return it
        """
        res = []
        for step in range(steps):
            row = start[0] + step * direction[0]
            col = start[1] + step * direction[1]
            res.append(self._grid[row][col])
        return res
    
    def modify(self , start , direction , steps , merged):
        """
        modifies the grid
        """
        for step in range(steps):
            row = start[0] + step * direction[0]
            col = start[1] + step * direction[1]
            self._grid[row][col] = merged[step]
        

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
            cutted = self.cut(index,OFFSETS[direction], steps)
            merged, score = merge(cutted)
            self.score += score
            if cutted != merged :
                changed = True
            self.modify(index,OFFSETS[direction], steps , merged)
        if changed:
            self.print_score()
            self.new_tile()

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
        else :
            self._grid[row][col] = 2
            
    def print_score(self):
        sys.stdout.write("Score: "+str(self.score)+"\r")
        sys.stdout.flush()    

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


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))