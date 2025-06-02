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
                    positions.append((x, y))
        return positions
        
    def insert_at_random_empty_space(self):
        position = random.choice(self.empty_positions())
        value = 2
        self.grid[position[1]][position[0]] = value

        
    def move_left(self):
        new_grid = []
        for row in self.grid:
            # remove empty spaces
            merged_row = [value for value in row if value != 0]
            
            # print(new_row, len(new_row))
            # merging neighbours with same value on the horizontal
            for index in range(len(merged_row) - 1):
                if merged_row[index] == merged_row[index + 1]:
                    merged_row[index] *= 2
                    merged_row[index + 1] = 0
            
            # remove empty spaces after merge
            merged_row = [value for value in merged_row if value != 0]
       
            # fill up the empty space
            while(len(merged_row) < self.grid_size):
                merged_row.append(0)
            
            new_grid.append(merged_row)
        self.grid = new_grid
        if self.has_empty_space():
            self.insert_at_random_empty_space()

    def move_right(self):
        new_grid = []
        for row in self.grid:
            # remove empty spaces
            new_row = [value for value in row if value != 0]

            # merging neighbours with same value on the horizontal
            for index in range(len(new_row) - 1):
                if new_row[index] == row[index + 1]:
                    new_row[index] *= 2
                    new_row[index + 1] = 0
            
            # remove empty spaces after merge
            new_row = [value for value in new_row if value != 0]
       
            # fill up the empty space
            while(len(new_row) < self.grid_size):
                new_row.insert(0, 0)
            
            new_grid.append(new_row)
        self.grid = new_grid      