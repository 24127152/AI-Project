import heapq
import math
import time
def UCS(grid, start, goal):
    start_time = time.perf_counter()

    rows, cols = len(grid), len(grid[0])

    explored_nodes = []




    end_time = time.perf_counter()
    return {
        "path_found": None,
        "explored_nodes_count": len(explored_nodes),
        "total_path_cost": math.inf,
        "processing_time_ms": round((end_time - start_time) * 1000, 4),
    }

if __name__ == "__main__":
    INF = math.inf # Wall
    grid = [
        [1, 1, 5, 1, 1],
        [1, 1, 5, 1, 1],
        [1, 1, 1, INF, 1],
        [INF, INF, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ]
    
    start_node = (0, 0)
    goal_node = (4, 4)
    
    result = UCS(grid, start_node, goal_node)
    
    print("--- DETAILED OUTPUT ---")
    print(f"- Path found: {result['path_found']}")
    print(f"- Number of explored nodes: {result['explored_nodes_count']}")
    print(f"- Total path cost: {result['total_path_cost']}")
    print(f"- Processing time: {result['processing_time_ms']} ms")