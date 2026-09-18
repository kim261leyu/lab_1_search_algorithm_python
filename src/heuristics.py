
def heuristic(candidates):
    for cell_candidates in candidates.values():
        if len(cell_candidates) == 0:
            return float('inf')
    return len(candidates)