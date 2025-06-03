import random

class GameLogic2048:
    def __init__(self, grid_size: int = 4):
        self.grid_size = grid_size
        self.points = 0

        self.game_over = False
    
        self.create_grid()

    def create_grid(self):
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        initial_positions = random.sample(self.empty_positions(), 2)

        first_position = initial_positions[0]
        second_position = initial_positions[1]

        self.grid[first_position[0]][first_position[1]] = 2
        self.grid[second_position[0]][second_position[1]] = self.generate_value()
        
    def generate_value(self) -> int:
        return 2 if random.randint(1, 100) < 90 else 4
    
    def restart(self):
        self.create_grid()
        self.points = 0

    def has_empty_space(self) -> bool:
        return any(0 in row for row in self.grid)
    
    def empty_positions(self):
        positions = []
        for y, row in enumerate(self.grid):
            for x, value in enumerate(row):
                if value == 0:
                    positions.append((y, x))
        return positions
        
    def insert_at_random_empty_space(self):
        if self.has_empty_space():
            position = random.choice(self.empty_positions())
            self.grid[position[0]][position[1]] = self.generate_value()
            return position

    def process_values(self, values: list[int]):
        values = [value for value in values if value != 0]

        for index, value in enumerate(values[:-1]):
            if value == values[index + 1]:
                values[index] = value * 2
                self.points += value * 2
                values[index + 1] = 0

        values = [value for value in values if value != 0]

        while(len(values) < self.grid_size):
            values.append(0)

        return values
    
    def move_left(self):
        new_grid = []
        for row in self.grid:
            new_grid.append(self.process_values(row))

        self.grid = new_grid

    def move_right(self):
        new_grid = []
        for row in self.grid:
            processed_row = self.process_values(row[::-1])
            new_grid.append(processed_row[::-1])

        self.grid = new_grid

    def move_up(self):
        new_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            row = [self.grid[j][i] for j in range(self.grid_size)]
            processed_row = self.process_values(row)

            for j in range(self.grid_size):
                new_grid[j][i] = processed_row[j]

        self.grid = new_grid
    
    def move_down(self):
        new_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            row = [self.grid[j][i] for j in range(self.grid_size)]
            processed_row = self.process_values(row[::-1])[::-1]

            for j in range(self.grid_size):
                new_grid[j][i] = processed_row[j]

        self.grid = new_grid