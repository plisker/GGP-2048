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


# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

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
        # self.prepare_terminal_output()
        self.score = 0
        self.final_print()
        # self.print_board()

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
            self.score += sum_score
            if cutted != merged:
                changed = True
            self.modify(index, OFFSETS[direction], steps, merged)
        if changed:
            self.new_tile()

            # TODO: Beautify print to terminal here!
            self.final_print()

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
            score += sum_score
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
            grid = None

        return grid, score

    def get_state(self):
        return self._grid

    def get_score(self):
        return self.score

    def legal_moves(self, grid):
        legal = []
        for i in xrange(4):
            test_grid = copy.deepcopy(grid)
            # self.alert("\nTesting move "+str(i+1)+"!")

            result, _ = self.get_successor(i+1, test_grid, 0)
            if result != None:
                legal.append(i+1)
                # self.alert("Move "+str(i+1)+" was appended as a legal move!") 

        # self.alert("All moves tested!")

        if legal == []:
            self.alert("No more moves!")
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
            
    def print_board(self):
        self.stdscr.clear()
        self.stdscr.addstr("Score: "+str(self.score)+"\n")       
        for row in self._grid:
            self.stdscr.addstr(str(row)+"\n")       
        self.stdscr.refresh()

    def final_print(self):
        print "Final Score: "+str(self.score)
        for row in self._grid:
            print row

    def end_game(self):
        # curses.endwin()
        print ""
        self.final_print()


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
        # self.stdscr.addstr(string+"\n")
        # self.stdscr.refresh()
        print string
        pass

def main():
    print "Run the game from main.py"

if __name__=='__main__':
        main()