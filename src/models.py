from dataclasses import dataclass, field

@dataclass
class SearchResult:
    algorithm: str
    path_cost: float
    path_length: int
    nodes_expanded: int
    max_frontier_size: int
    execution_time_ms: float
    peak_memory_kb: float
    success: bool
    

@dataclass(order=True)
class AStarNode:
    f_cost: float
    g_cost: float = field(compare=False)
    grid: tuple = field(compare=False)
    candidates: dict = field(compare=False)  
    

