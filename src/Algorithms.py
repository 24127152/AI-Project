import heapq
import math
import time

def Heuristic(node, goal):
    # Sử dụng Manhattan distance làm heuristic
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def UCS(grid, start, goal):
    start_time = time.perf_counter()

    rows, cols = len(grid), len(grid[0])

    priority_queue = [(0, start, [start])]
    explored_nodes = set()
    max_queue_size = 0

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while priority_queue:
        if len(priority_queue) > max_queue_size:
            max_queue_size = len(priority_queue)

        current_cost, current_node, path = heapq.heappop(priority_queue)

        if current_node in explored_nodes:
            continue

        explored_nodes.add(current_node)

        if current_node == goal:
            end_time = time.perf_counter()
            return {
                "path_found": path,
                "explored_nodes_count": len(explored_nodes),
                "total_path_cost": current_cost,
                "max_queue_size": max_queue_size,
                "processing_time_ms": round((end_time - start_time) * 1000, 4),
            }
        
        for dr, dc in directions:
            neighbor = (current_node[0] + dr, current_node[1] + dc)

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                step_cost = grid[neighbor[0]][neighbor[1]]
                
                # Bỏ qua nếu là tường (INF)
                if step_cost != math.inf and neighbor not in explored_nodes:
                    new_cost = current_cost + step_cost
                    heapq.heappush(priority_queue, (new_cost, neighbor, path + [neighbor]))
                
    end_time = time.perf_counter()
    return {
        "path_found": None,
        "explored_nodes_count": len(explored_nodes),
        "total_path_cost": math.inf,
        "max_queue_size": max_queue_size,
        "processing_time_ms": round((end_time - start_time) * 1000, 4),
    }


def A_search(grid, start, goal):
    start_time = time.perf_counter()

    rows, cols = len(grid), len(grid[0])
    # Queue: (f_cost, g_cost, node, path)
    priority_queue = [(Heuristic(start, goal), 0, start, [start])]

    explored_nodes = set()
    max_queue_size = 0

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while priority_queue:
        if len(priority_queue) > max_queue_size:
            max_queue_size = len(priority_queue)
        current_f_cost, current_g_cost, current_node, path = heapq.heappop(priority_queue)

        if current_node in explored_nodes:
            continue

        explored_nodes.add(current_node)

        if current_node == goal:
            end_time = time.perf_counter()
            return {
                "path_found": path,
                "explored_nodes_count": len(explored_nodes),
                "total_path_cost": current_g_cost,
                "max_queue_size": max_queue_size,
                "processing_time_ms": round((end_time - start_time) * 1000, 4),
            }
        
        for dr, dc in directions:
            neighbor = (current_node[0] + dr, current_node[1] + dc)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                step_cost = grid[neighbor[0]][neighbor[1]]
                if step_cost != math.inf and neighbor not in explored_nodes:
                    new_g_cost = current_g_cost + step_cost
                    new_f_cost = new_g_cost + Heuristic(neighbor, goal)
                    heapq.heappush(priority_queue, (new_f_cost, new_g_cost, neighbor, path + [neighbor]))

    end_time = time.perf_counter()
    return {
        "path_found": None,
        "explored_nodes_count": len(explored_nodes),
        "total_path_cost": math.inf,
        "max_queue_size": max_queue_size,
        "processing_time_ms": round((end_time - start_time) * 1000, 4),
    }

def Form(grid, start, goal):
    start_time = time.perf_counter()

    rows, cols = len(grid), len(grid[0])

    explored_nodes = set()
    max_queue_size = 0 #memory usage


    end_time = time.perf_counter()
    return {
        "path_found": None,
        "explored_nodes_count": len(explored_nodes),
        "total_path_cost": math.inf,
        "max_queue_size": max_queue_size,
        "processing_time_ms": round((end_time - start_time) * 1000, 4),
    }

if __name__ == "__main__":
    INF = math.inf # Wall
    grid = [
        [1,   1,   1,   1,   INF, 1,   1,   1,   1,   1  ],
        [1,   5,   5,   1,   INF, 1,   5,   5,   5,   1  ],
        [1,   INF, 1,   1,   INF, 1,   1,   1,   INF, 1  ],
        [1,   INF, 1,   5,   5,   5,   INF, 1,   INF, 1  ],
        [1,   1,   1,   INF, INF, 1,   INF, 1,   INF, 1  ],
        [INF, INF, 1,   1,   1,   1,   INF, 1,   1,   1  ],
        [1,   1,   5,   5,   5,   1,   INF, INF, INF, 1  ],
        [1,   INF, INF, INF, 1,   1,   1,   1,   1,   1  ],
        [1,   1,   1,   INF, 5,   5,   5,   INF, 5,   1  ],
        [INF, INF, 1,   1,   1,   1,   1,   1,   1,   1  ]
    ]
    
    start_node = (0, 0)
    goal_node = (9, 9)

    result = A_search(grid, start_node, goal_node)
    
    print("--- DETAILED OUTPUT ---")
    print(f"- Path found: {result['path_found']}")
    print(f"- Number of explored nodes: {result['explored_nodes_count']}")
    print(f"- Total path cost: {result['total_path_cost']}")
    print(f"- Max Queue Size: {result['max_queue_size']}")
    print(f"- Processing time: {result['processing_time_ms']} ms")