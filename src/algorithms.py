from src.heuristics import heuristic
from src.models import AStarNode

import heapq



def dfs_backtrack(env, nodes_exp_counter, depth_tracker, depth=0):
    
    depth_tracker[0] = max(depth_tracker[0], depth);
    if env.is_complete():
        return True
        
    row, col = env.find_first_empty();
    candidates = env.get_candidates(row, col);
    for digit in candidates:
        env.place(row, col, digit);
        nodes_exp_counter[0] += 1;
        if dfs_backtrack(env, nodes_exp_counter, depth_tracker, depth + 1):
            return True;
        env.undo(row, col, digit);
    return False;
        

    
def mrv_backtrack(env, nodes_exp_counter, depth_tracker, depth=0):
    
    depth_tracker[0] = max(depth_tracker[0], depth);
    if env.is_complete():
        return True
        
    (row, col), candidates = env.find_mrv_cell();
    
    
    for digit in candidates:
        env.place(row, col, digit);
        nodes_exp_counter[0] += 1;
        if mrv_backtrack(env, nodes_exp_counter, depth_tracker, depth + 1):
            return True;
        env.undo(row, col, digit);
    return False;
    
    
    
def build_initial_candidates(grid, size, box_size):

    candidate_dict = dict();
    all_numbers = set(range(1, size + 1));
    
    for row in range(size):
        for col in range(size):
            if grid[row][col] == 0:
                used_numbers = set();
                box_row = (row // box_size) * box_size;
                box_col = (col // box_size) * box_size;
                for cell in range(size):
                    used_numbers.add(grid[row][cell]);
                    used_numbers.add(grid[cell][col]);
                    
                    r_box = (cell % box_size) + box_row
                    c_box = (cell // box_size) + box_col
                    used_numbers.add(grid[r_box][c_box])
             
                candidates = all_numbers - used_numbers;
                candidate_dict[(row, col)] = candidates;
                
    return candidate_dict

def derive_child_candidates(parent_candidates, grid, size, box_size, row, col, digit):
    
    new_candidates = parent_candidates.copy();
    del new_candidates[(row, col)];
    
    box_row = (row // box_size) * box_size;
    box_col = (col // box_size) * box_size;
    for cell in range(size):
        if grid[row][cell] == 0 and cell != col:
            new_candidates[(row, cell)] = new_candidates[(row, cell)] - {digit};
        if grid[cell][col] == 0 and cell != row:
            new_candidates[(cell, col)] = new_candidates[(cell, col)] - {digit};
        
        r_box = (cell % box_size) + box_row
        c_box = (cell // box_size) + box_col
        if grid[r_box][c_box] == 0 and (r_box, c_box) != (row, col):
            new_candidates[(r_box, c_box)] = new_candidates[(r_box, c_box)] - {digit};
    
             
    return new_candidates;
    



def find_mrv_cell_a_star(candidates_dict, size):
    best_key = None;
    best_candidates = None;
    smallest_count = None;
    for key, value in candidates_dict.items():
        candidate_len = len(value);
        if candidate_len == 1:
            return key, value;
        if smallest_count is None or candidate_len < smallest_count:
            smallest_count = candidate_len;
            best_key = key;
            best_candidates = value;
            
    return best_key, best_candidates
        
def find_first_empty_cell_a_star(candidates_dict, size):
    if not candidates_dict:
        return None, None
        
    
    first_key = next(iter(candidates_dict))
    return first_key, candidates_dict[first_key]

def place_copy(grid, row, col, digit):

    new_grid = list(grid);
    new_row = list(new_grid[row]);
    new_row[col] = digit;
    new_grid[row] = tuple(new_row);

    return tuple(new_grid);


def astar_search(initial_grid, size, box_size, nodes_exp_counter, max_frontier_tracker):

    candidates_dict = build_initial_candidates(initial_grid, size, box_size);
    g = 0;
    h = heuristic(candidates_dict);
    f = g + h;
    start_node = AStarNode(f_cost=f, g_cost=g, grid=initial_grid, candidates=candidates_dict);
    
    frontier = []
    heapq.heappush(frontier, start_node);
    
    while frontier:
        max_frontier_tracker[0] = max(max_frontier_tracker[0], len(frontier));
        
        current = heapq.heappop(frontier);
        
        if len(current.candidates) == 0:
            return current;
            
        row_col, candidates = find_first_empty_cell_a_star(current.candidates, size);
        
        row, col = row_col;
        
        for digit in candidates:
            nodes_exp_counter[0] += 1;
            new_grid = place_copy(current.grid, row, col, digit);
            new_candidates = derive_child_candidates(current.candidates, current.grid, size, box_size, row, col, digit);
            new_h = heuristic(new_candidates);
            
            if new_h != float('inf'):
                new_g = current.g_cost + 1;
                new_f = new_g + new_h;
                child_node = AStarNode(f_cost=new_f, g_cost=new_g, grid=new_grid, candidates=new_candidates);
                heapq.heappush(frontier, child_node);
                
    return None;
            
            
    