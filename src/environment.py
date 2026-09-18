class SudokuEnvironment:
    
    def __init__(self, grid):
        self.grid = grid
        self.size = len(grid)          
        self.box_size = 3              
        self.all_digits = set(range(1, self.size + 1));

        self.row_used = [set() for _ in range(self.size)]
        self.col_used = [set() for _ in range(self.size)]
        self.box_used = [set() for _ in range(self.size)]
        
        self.empty_slots = sum(row.count(0) for row in grid);

        self._init_constraints()

    def _init_constraints(self):
        for row in range(self.size):
            for col in range(self.size):
                digit = self.grid[row][col];
                if digit != 0:
                    self._add_digit(row, col, digit);
        

    def _box_index(self, row, col):
        box_index = (row // 3) * 3 + (col // 3);
        return box_index        
        

    def get_candidates(self, row, col):
        box = self._box_index(row, col);
        candidates = self.all_digits - (self.row_used[row] | self.col_used[col] | self.box_used[box]);
        return candidates

    def place(self, row, col, digit):
        self.grid[row][col] = digit;
        self._add_digit(row, col, digit);
        self.empty_slots -= 1;
        
    def _add_digit(self, row, col, digit):
        box = self._box_index(row, col)
        self.row_used[row].add(digit)
        self.col_used[col].add(digit)
        self.box_used[box].add(digit)

    def undo(self, row, col, digit):
        self.grid[row][col] = 0;
        box = self._box_index(row, col);
        self.row_used[row].discard(digit);
        self.col_used[col].discard(digit);
        self.box_used[box].discard(digit);
        self.empty_slots += 1;
        

    def is_complete(self):
        return self.empty_slots == 0;
        
    def is_valid_solution(self):
        if not self.is_complete():
            return False

        full_set = set(range(1, self.size + 1))

        for row in self.grid:
            if set(row) != full_set:
                return False

        for col in range(self.size):
            column_values = [self.grid[row][col] for row in range(self.size)]
            if set(column_values) != full_set:
                return False

        for box_row in range(0, self.size, self.box_size):
            for box_col in range(0, self.size, self.box_size):
                box_values = []
                for r in range(box_row, box_row + self.box_size):
                    for c in range(box_col, box_col + self.box_size):
                        box_values.append(self.grid[r][c])
                if set(box_values) != full_set:
                    return False

        return True
        
    def place_copy(grid, row, col, digit):
        new_grid = [list(r) for r in grid]  
        new_grid[row][col] = digit
        return tuple(tuple(r) for r in new_grid)
        
    def find_mrv_cell(self):
        best_row = None;
        best_col = None;
        best_candidates = None;
        smallest_candidates = self.size + 1;
        
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    candidates = self.get_candidates(row, col);
                    if smallest_candidates > len(candidates):
                        best_row = row;
                        best_col = col;
                        smallest_candidates = len(candidates);
                        best_candidates = candidates;
                
                
        return (best_row, best_col), best_candidates;
        
        
    def find_first_empty(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    return row, col;
        return None;
        
