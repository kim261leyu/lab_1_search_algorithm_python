from src.minheap import IndexedHeap

def mrv_optimized(env, min_heap, nodes_exp_counter, depth_tracker, depth=0):
    
    depth_tracker[0] = max(depth_tracker[0], depth);
    if env.is_complete():
        return True
        
    placed_singles = []
    while True:
        count, row, col = min_heap.peek_min()
        if count == 0:
            for r, c, d in reversed(placed_singles):
                undo_and_sync(env, min_heap, r, c, d)
            return False
        if count == 1:
            break
        singles = hidden_singles(env, row, col)
        if not singles:
            break

        digit, r, c = singles.pop()
        place_and_sync(env, min_heap, r, c, digit)
        placed_singles.append((r, c, digit))
        nodes_exp_counter[0] += 1
        if env.is_complete():
            return True
            
    candidates = env.get_candidates(row, col);
    
    
    for digit in candidates:
        place_and_sync(env, min_heap, row, col, digit);
        nodes_exp_counter[0] += 1;
        if mrv_optimized(env, min_heap, nodes_exp_counter, depth_tracker, depth + 1):
            return True;
        undo_and_sync(env, min_heap, row, col, digit);
    for r, c, d in reversed(placed_singles):
        undo_and_sync(env, min_heap, r, c, d)
    return False;
    
    
def build_heap(env):
    min_heap =  IndexedHeap()
    for row in range(env.size):
        for col in range(env.size):
            digit = env.grid[row][col];
            if digit == 0:
                candidates = env.get_candidates(row, col);
                
                min_heap.push(row, col, len(candidates));
                
    return min_heap

    
    
def peers(row, col, size, box_size):
    peers = set()
    box_row = (row // box_size) * box_size;
    box_col = (col // box_size) * box_size;
    for cell in range(size):
        peers.add((row, cell))
        peers.add((cell, col))
        
        r_box = (cell % box_size) + box_row
        c_box = (cell // box_size) + box_col
        
        peers.add((r_box, c_box));
        
    peers.discard((row, col));
    
    return peers;
    
def place_and_sync(env, heap, row, col, digit):
    heap.delete(row, col)
    env.place(row, col, digit)
    for prow, pcol in peers(row, col, env.size, env.box_size):
        if env.grid[prow][pcol] == 0:
            heap.update(prow, pcol, len(env.get_candidates(prow, pcol)))
            
            
def undo_and_sync(env, heap, row, col, digit):
    env.undo(row, col, digit);
    heap.push(row, col, len(env.get_candidates(row, col)));
    for prow, pcol in peers(row, col, env.size, env.box_size):
        if env.grid[prow][pcol] == 0:
            heap.update(prow, pcol, len(env.get_candidates(prow, pcol)));
            
            
            
def hidden_singles(env, row, col):
    singles_row = [0 for _ in range(0, env.size + 1)]
    cell_of_row = [None for _ in range(0, env.size + 1)]
    
    singles_col = [0 for _ in range(0, env.size + 1)]
    cell_of_col = [None for _ in range(0, env.size + 1)]
    
    singles_block = [0 for _ in range(0, env.size + 1)]
    cell_of_block = [None for _ in range(0, env.size + 1)]
    
    
    box_row = (row // env.box_size) * env.box_size;
    box_col = (col // env.box_size) * env.box_size;
    
    
    for cell in range(env.size):
        if env.grid[row][cell] == 0:
            candidates_row = env.get_candidates(row, cell);
            for candidate in candidates_row:
                singles_row[candidate] += 1;
                cell_of_row[candidate] = cell;
        if env.grid[cell][col] == 0:
            candidates_col = env.get_candidates(cell, col);
            for candidate in candidates_col:
                singles_col[candidate] += 1;
                cell_of_col[candidate] = cell;
                
        r_box = (cell % env.box_size) + box_row
        c_box = (cell // env.box_size) + box_col
        
        if env.grid[r_box][c_box] == 0:
            candidates_block = env.get_candidates(r_box, c_box);
            for candidate in candidates_block:
                singles_block[candidate] += 1;
                cell_of_block[candidate] = (r_box, c_box);
                
    result = list()
    
    for i in range(1, env.size + 1):
        if singles_row[i] == 1:
            result.append((i, row, cell_of_row[i]))
        if singles_col[i] == 1:
            result.append((i, cell_of_col[i], col))
        if singles_block[i] == 1:
            result.append((i, cell_of_block[i][0], cell_of_block[i][1]))
   
    return result
    
    
