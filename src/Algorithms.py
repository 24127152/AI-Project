import heapq
import math
import time

WALL_VALUE = 1
WALKABLE_VALUES = {0, 2, 3}


def Heuristic(node, goal):
    # Sử dụng Manhattan distance làm heuristic
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def UCS(grid, start, goal):
    start_time = time.perf_counter()

    if not grid or not grid[0]:
        return {
            "path_found": None,
            "explored_nodes_count": 0,
            "total_path_cost": math.inf,
            "max_queue_size": 0,
            "processing_time_ms": 0,
        }

    rows, cols = len(grid), len(grid[0])

    priority_queue = [(0, start, [start])]
    explored_nodes = set()
    exploration_order = []
    max_queue_size = 0

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while priority_queue:
        if len(priority_queue) > max_queue_size:
            max_queue_size = len(priority_queue)

        current_cost, current_node, path = heapq.heappop(priority_queue)

        if current_node in explored_nodes:
            continue

        explored_nodes.add(current_node)
        exploration_order.append(current_node)

        if current_node == goal:
            end_time = time.perf_counter()
            return {
                "path_found": path,
                "exploration_order": exploration_order,
                "explored_nodes_count": len(explored_nodes),
                "total_path_cost": current_cost,
                "max_queue_size": max_queue_size,
                "processing_time_ms": round((end_time - start_time) * 1000, 4),
            }
        
        for dr, dc in directions:
            neighbor = (current_node[0] + dr, current_node[1] + dc)

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                neighbor_value = grid[neighbor[0]][neighbor[1]]
                
                if neighbor_value in WALKABLE_VALUES and neighbor not in explored_nodes:
                    step_cost = 1
                    new_cost = current_cost + step_cost
                    heapq.heappush(priority_queue, (new_cost, neighbor, path + [neighbor]))
                
    end_time = time.perf_counter()
    return {
        "path_found": None,
        "exploration_order": exploration_order,
        "explored_nodes_count": len(explored_nodes),
        "total_path_cost": math.inf,
        "max_queue_size": max_queue_size,
        "processing_time_ms": round((end_time - start_time) * 1000, 4),
    }


def A_search(grid, start, goal):
    start_time = time.perf_counter()

    if not grid or not grid[0]:
        return {
            "path_found": None,
            "explored_nodes_count": 0,
            "total_path_cost": math.inf,
            "max_queue_size": 0,
            "processing_time_ms": 0,
        }

    rows, cols = len(grid), len(grid[0])
    # Queue: (f_cost, g_cost, node, path)
    priority_queue = [(Heuristic(start, goal), 0, start, [start])]

    explored_nodes = set()
    exploration_order = []
    max_queue_size = 0

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while priority_queue:
        if len(priority_queue) > max_queue_size:
            max_queue_size = len(priority_queue)
        current_f_cost, current_g_cost, current_node, path = heapq.heappop(priority_queue)

        if current_node in explored_nodes:
            continue

        explored_nodes.add(current_node)
        exploration_order.append(current_node)

        if current_node == goal:
            end_time = time.perf_counter()
            return {
                "path_found": path,
                "exploration_order": exploration_order,
                "explored_nodes_count": len(explored_nodes),
                "total_path_cost": current_g_cost,
                "max_queue_size": max_queue_size,
                "processing_time_ms": round((end_time - start_time) * 1000, 4),
            }
        
        for dr, dc in directions:
            neighbor = (current_node[0] + dr, current_node[1] + dc)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                neighbor_value = grid[neighbor[0]][neighbor[1]]
                if neighbor_value in WALKABLE_VALUES and neighbor not in explored_nodes:
                    step_cost = 1
                    new_g_cost = current_g_cost + step_cost
                    new_f_cost = new_g_cost + Heuristic(neighbor, goal)
                    heapq.heappush(priority_queue, (new_f_cost, new_g_cost, neighbor, path + [neighbor]))

    end_time = time.perf_counter()
    return {
        "path_found": None,
        "exploration_order": exploration_order,
        "explored_nodes_count": len(explored_nodes),
        "total_path_cost": math.inf,
        "max_queue_size": max_queue_size,
        "processing_time_ms": round((end_time - start_time) * 1000, 4),
    }

def Beam_search(grid, start, goal, beam_width=2):
    start_time = time.perf_counter()

    if not grid or not grid[0]:
        return {
            "path_found": None,
            "explored_nodes_count": 0,
            "total_path_cost": math.inf,
            "max_queue_size": 0,
            "processing_time_ms": 0,
        }

    rows, cols = len(grid), len(grid[0])

    explored_nodes = set()
    exploration_order = []
    max_queue_size = 0 

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # beam lưu trữ danh sách các node đang xét
    # Cấu trúc: (f_cost, g_cost, node, path)
    beam = [(Heuristic(start, goal), 0, start, [start])]

    while beam:
        next_beam = []
        
        for current_f_cost, current_g_cost, current_node, path in beam:
            if current_node in explored_nodes:
                continue

            explored_nodes.add(current_node)
            exploration_order.append(current_node)

            if current_node == goal:
                end_time = time.perf_counter()
                return {
                    "path_found": path,
                    "exploration_order": exploration_order,
                    "explored_nodes_count": len(explored_nodes),
                    "total_path_cost": current_g_cost,
                    "max_queue_size": max_queue_size,
                    "processing_time_ms": round((end_time - start_time) * 1000, 4),
                }

            # Sinh các node kề
            for dr, dc in directions:
                neighbor = (current_node[0] + dr, current_node[1] + dc)

                if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                    neighbor_value = grid[neighbor[0]][neighbor[1]]
                    
                    if neighbor_value in WALKABLE_VALUES and neighbor not in explored_nodes:
                        step_cost = 1
                        new_g_cost = current_g_cost + step_cost
                        new_f_cost = new_g_cost + Heuristic(neighbor, goal)
                        next_beam.append((new_f_cost, new_g_cost, neighbor, path + [neighbor]))

        # Cập nhật max_queue_size dựa trên số lượng node sinh ra trước khi bị cắt tỉa
        if len(next_beam) > max_queue_size:
            max_queue_size = len(next_beam)

        # Sắp xếp các node kề mới sinh ra theo f_cost tăng dần
        next_beam.sort(key=lambda x: x[0])

        # Cắt tỉa (Pruning): Chỉ giữ lại 'beam_width' node tốt nhất cho bước tiếp theo
        beam = []
        seen_in_next = set()
        for item in next_beam:
            node = item[2]
            # Tránh thêm các node trùng lặp vào beam mới
            if node not in seen_in_next:
                seen_in_next.add(node)
                beam.append(item)
                if len(beam) == beam_width:
                    break

    end_time = time.perf_counter()
    return {
        "path_found": None,
        "exploration_order": exploration_order,
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