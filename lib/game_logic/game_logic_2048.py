import random

class GameLogic2048:
    def __init__(self, grid_size: int = 4):
        self.grid_size = grid_size

        self.start_fresh()

    def create_grid(self):
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        initial_positions = random.sample(self.empty_positions(), 2)

        first_position = initial_positions[0]
        second_position = initial_positions[1]

        self.grid[first_position[0]][first_position[1]] = 2
        self.grid[second_position[0]][second_position[1]] = self.generate_value()
        
    def generate_value(self) -> int:
        return 2 if random.randint(1, 100) < 90 else 4
    
    def start_fresh(self):
        self.points = 0
        self.moves = 0
        self.no_moves_left = False
        self.create_grid()

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

        result = []
        skip = False

        for i in range(len(values)):
            if skip:
                skip = False
                continue

            if i + 1 < len(values) and values[i] == values[i + 1]:
                merged_value = values[i] * 2
                result.append(merged_value)
                self.points += merged_value
                skip = True  # skip next value since it was merged
            else:
                result.append(values[i])

        while(len(result) < self.grid_size):
            result.append(0)

        return result
    
    def has_available_move(self):
        return self.can_move_down() or self.can_move_left() or self.can_move_right() or self.can_move_up()
    
    def can_move_left(self):
        for row in self.grid:
            processed_row = self.process_values(row)
            if row != processed_row:
                return True
        return False
    
    def move_left(self):
        new_grid = []
        changed = False

        for row in self.grid:
            processed_row = self.process_values(row)
            if row != processed_row:
                changed = True
            new_grid.append(processed_row)
        if changed:
            self.moves += 1
            self.grid = new_grid
        
        if not self.no_moves_left:
            self.no_moves_left = not self.has_available_move()

    def can_move_right(self):
        for row in self.grid:
            inverted_row = row[::-1]
            processed_row = self.process_values(inverted_row)[::-1]
            if row != processed_row:
                return True
        return False

    def move_right(self):
        new_grid = []
        changed = False

        for row in self.grid:
            inverted_row = row[::-1]
            processed_row = self.process_values(inverted_row)[::-1]
            if row != processed_row:
                changed = True
            new_grid.append(processed_row)

        if changed:
            self.moves += 1
            self.grid = new_grid

        if not self.no_moves_left:
            self.no_moves_left = not self.has_available_move()

    def can_move_up(self):
        for i in range(self.grid_size):
            row = [self.grid[j][i] for j in range(self.grid_size)]
            processed_row = self.process_values(row)
            if row != processed_row:
                return True
        return False

    def move_up(self):
        new_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        changed = False

        for i in range(self.grid_size):
            row = [self.grid[j][i] for j in range(self.grid_size)]
            processed_row = self.process_values(row)
            
            if row != processed_row:
                changed = True

            for j in range(self.grid_size):
                new_grid[j][i] = processed_row[j]

        if changed:
            self.moves += 1
            self.grid = new_grid
        
        if not self.no_moves_left:
            self.no_moves_left = not self.has_available_move()
    
    def can_move_down(self):
        for i in range(self.grid_size):
            row = [self.grid[j][i] for j in range(self.grid_size)]
            inverted_row = row[::-1]
            processed_row = self.process_values(inverted_row)[::-1]
            if row != processed_row:
                return True
        return False

    def move_down(self):
        new_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        changed = False

        for i in range(self.grid_size):
            row = [self.grid[j][i] for j in range(self.grid_size)]
            inverted_row = row[::-1]
            processed_row = self.process_values(inverted_row)[::-1]

            if row != processed_row:
                changed = True

            for j in range(self.grid_size):
                new_grid[j][i] = processed_row[j]

        if changed:
            self.moves += 1
            self.grid = new_grid

        if not self.no_moves_left:
            self.no_moves_left = not self.has_available_move()