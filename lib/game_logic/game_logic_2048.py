import random

class GameLogic2048:
    def __init__(self, grid_size: int = 4):
        self.grid_size = 4

        self.create_grid()

    def create_grid(self):
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        self.grid[0][0] = 2
        self.grid[0][3] = 2

    def has_empty_space(self):
        return any(0 in row for row in self.grid)
    
    def empty_positions(self):
        positions = []
        for y, row in enumerate(self.grid):
            for x, value in enumerate(row):
                if value == 0:
                    positions.append((y, x))
        return positions
        
    def insert_at_random_empty_space(self):
        position = random.choice(self.empty_positions())
        value = 2
        self.grid[position[0]][position[1]] = value

    # Moves the grid in the horizontal axis.
    # By default it moves to the left, if moving to the right
    # we invert the row, move to the left and invert back.   
    def move_horizontal(self, move_right: bool = False):
        new_grid = []
        for row in self.grid:
            # remove empty spaces
            merged_row = [value for value in row if value != 0]

            # if its a move to the right, we first invert the row
            if move_right:
                merged_row = merged_row[::-1]
            
            # merging neighbours with same value on the horizontal
            for index, value in enumerate(merged_row[:-1]):
                if value == merged_row[index + 1]:
                    merged_row[index] = value * 2
                    merged_row[index + 1] = 0
            
            # remove empty spaces after merge
            merged_row = [value for value in merged_row if value != 0]
       
            # fill up the empty space
            while(len(merged_row) < self.grid_size):
                merged_row.append(0)

            # if its a move to the right we need to invert back the row
            if move_right:
                merged_row = merged_row[::-1]
            
            new_grid.append(merged_row)

        self.grid = new_grid
        if self.has_empty_space():
            self.insert_at_random_empty_space()

    def move_vertical(self):
        pass