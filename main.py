import json
import yaml
import time
import tracemalloc
import copy
import pandas as pd

from src.environment import SudokuEnvironment
from src.algorithms import dfs_backtrack, mrv_backtrack, astar_search
from src.models import SearchResult
from src.mrv_optimized import mrv_optimized, build_heap



def load_config(path="config/config.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)

def load_grid(difficulty="easy", path="data/grid_map.json"):
    with open(path) as f:
        data = json.load(f)
    return data["puzzles"][difficulty]


def run_dfs_logic(grid):
    env = SudokuEnvironment(grid)
    initial_empty = env.empty_slots
    nodes, depth = [0], [0]
    success = dfs_backtrack(env, nodes, depth)
    return {
        'path_cost': initial_empty, 'nodes': nodes[0], 
        'max_frontier': depth[0], 'success': success
    }

def run_mrv_logic(grid):
    env = SudokuEnvironment(grid)
    initial_empty = env.empty_slots
    nodes, depth = [0], [0]
    success = mrv_backtrack(env, nodes, depth)
    return {
        'path_cost': initial_empty, 'nodes': nodes[0], 
        'max_frontier': depth[0], 'success': success
    }

def run_astar_logic(grid):
    size, box_size = len(grid), 3
    nodes, max_f = [0], [0]
    result_node = astar_search(grid, size, box_size, nodes, max_f)
    success = result_node is not None
    return {
        'path_cost': result_node.g_cost if success else 0, 'nodes': nodes[0], 
        'max_frontier': max_f[0], 'success': success, 'extra_data': result_node.grid if success else None
    }

def run_opt_logic(grid):
    env = SudokuEnvironment(grid)
    initial_empty = env.empty_slots
    heap = build_heap(env)
    nodes, depth = [0], [0]
    success = mrv_optimized(env, heap, nodes, depth)
    return {
        'path_cost': initial_empty, 'nodes': nodes[0], 
        'max_frontier': depth[0], 'success': success, 'extra_data': env
    }


def measure_and_run(name, algo_fn, grid):
    tracemalloc.start()
    start_time = time.perf_counter()
    
    metrics = algo_fn(grid)
    
    exec_time_ms = (time.perf_counter() - start_time) * 1000
    _, peak_mem_kb = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    result = build_result(
        algorithm=name, path_cost=metrics['path_cost'], 
        nodes_expanded=metrics['nodes'], max_frontier=metrics['max_frontier'],
        exec_time_ms=exec_time_ms, peak_mem_kb=peak_mem_kb, success=metrics['success']
    )
    return result, metrics.get('extra_data')



def build_result(algorithm, path_cost, nodes_expanded, max_frontier, exec_time_ms, peak_mem_kb, success):
    return SearchResult(
        algorithm=algorithm, path_cost=path_cost, path_length=path_cost, 
        nodes_expanded=nodes_expanded, max_frontier_size=max_frontier,
        execution_time_ms=exec_time_ms, peak_memory_kb=peak_mem_kb, success=success
    )
    
def average_results(results_list):
    n = len(results_list)
    return SearchResult(
        algorithm=results_list[0].algorithm,
        path_cost=sum(r.path_cost for r in results_list) / n,
        path_length=sum(r.path_length for r in results_list) / n,
        nodes_expanded=sum(r.nodes_expanded for r in results_list) / n,
        max_frontier_size=sum(r.max_frontier_size for r in results_list) / n,
        execution_time_ms=sum(r.execution_time_ms for r in results_list) / n,
        peak_memory_kb=sum(r.peak_memory_kb for r in results_list) / n,
        success=all(r.success for r in results_list)
    )


def print_results(results, as_table=True):
    if as_table:
        df = pd.DataFrame([r.__dict__ for r in results])
        df.columns = ['Algorithm', 'Path Cost', 'Path Length', 'Nodes Expanded',
                      'Max Frontier', 'Time (ms)', 'Peak Mem (KB)', 'Success']
        print(df.to_string(index=False))
    else:
        for r in results:
            print(f"{r.algorithm}:")
            print(f"  Time:  {r.execution_time_ms:.2f} ms")
            print(f"  Space: {r.peak_memory_kb:.2f} KB")


def run_multiple_times_and_average(name, algo_fn, grid, num_runs=3):

    results = []
    
    for _ in range(num_runs):
        result, _ = measure_and_run(name, algo_fn, copy.deepcopy(grid))
        results.append(result)
        
    return average_results(results)

def main():
    difficulties = ["easy", "medium", "hard", "expert", "master", 
                    "extreme", "everest", "escargot", "platinum_blonde"]
    
    algorithms = {
        "Backtracking DFS": run_dfs_logic,
        "Backtracking + MRV": run_mrv_logic,
        "A*": run_astar_logic,
        "opt": run_opt_logic
    }
    
    all_results = {name: [] for name in algorithms}
    
    for difficulty in difficulties:
        grid = load_grid(difficulty)
        current_run_results = []
        
        print(f"\n=== {difficulty.upper()} ===")
        
        for name, algo_fn in algorithms.items():
            result, _ = measure_and_run(name, algo_fn, copy.deepcopy(grid))
            current_run_results.append(result)
            all_results[name].append(result)
            
        print_results(current_run_results)
    
    avg_results = [average_results(all_results[name]) for name in algorithms]
    
    print("\n=== AVERAGE ACROSS ALL DIFFICULTIES ===")
    print_results(avg_results)
    print()

    grid = load_grid("unsolvable_28")
    print("\n=== Testing unsolvable_28 ===")
    
    unsolvable_results = []
    for name, algo_fn in algorithms.items():
        if name in ["Backtracking DFS", "A*"]:
            continue
            
        result, env = measure_and_run(name, algo_fn, copy.deepcopy(grid))
        unsolvable_results.append(result)
        
                
    print_results(unsolvable_results)
    
   

if __name__ == "__main__":
    main()