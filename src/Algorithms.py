import heapq
import math
import time
from collections import deque

WALL_VALUE = 1
MONSTER_COST_VALUE = 5
PLANT_COST_VALUE = 6
WALKABLE_VALUES = {0, 2, 3, MONSTER_COST_VALUE, PLANT_COST_VALUE}


def get_cell_cost(cell_value):
    if cell_value == MONSTER_COST_VALUE:
        return MONSTER_COST_VALUE
    if cell_value == PLANT_COST_VALUE:
        return PLANT_COST_VALUE
    return 1


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
                    step_cost = get_cell_cost(neighbor_value)
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
                    step_cost = get_cell_cost(neighbor_value)
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
                        step_cost = get_cell_cost(neighbor_value)
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


#IDA 
def get_cell_cost(cell_value):
    if cell_value == MONSTER_COST_VALUE:
        return MONSTER_COST_VALUE
    if cell_value == PLANT_COST_VALUE:
        return PLANT_COST_VALUE
    return 1


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def dfs_search(matrix, start, goal, g, threshold, path, exploration_order, explored_nodes):
    current = path[-1]
    if current not in explored_nodes:
        explored_nodes.add(current)
        exploration_order.append(current)

    f = g + heuristic(current, goal)
    if f > threshold:
        return f
    if current == goal:
        return True
    min_threshold = float('inf')
    for move in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        next_node = (current[0] + move[0], current[1] + move[1])
        if 0 <= next_node[0] < len(matrix) and 0 <= next_node[1] < len(matrix[0]) and next_node not in path:
            cell = matrix[next_node[0]][next_node[1]]
            if cell in (0, 2, 3, MONSTER_COST_VALUE, PLANT_COST_VALUE) or next_node == goal:
                path.append(next_node)
                #Backtracking
                temp = dfs_search(matrix, start, goal, g + get_cell_cost(cell), threshold, path, exploration_order, explored_nodes)
                if temp == True:
                    return True
                if temp < min_threshold:
                    min_threshold = temp
                path.pop()
    return min_threshold

def ida_star(matrix, start, goal, return_details=False):
    start_time = time.perf_counter()
    threshold = heuristic(start, goal)
    path = [start]
    exploration_order = []
    explored_nodes = set()

    while True:
        temp = dfs_search(matrix, start, goal, 0, threshold, path, exploration_order, explored_nodes)
        if temp == True:
            end_time = time.perf_counter()
            if return_details:
                return {
                    "path_found": path,
                    "exploration_order": exploration_order,
                    "explored_nodes_count": len(explored_nodes),
                    "processing_time_ms": round((end_time - start_time) * 1000, 4),
                }
            return path
        if temp == float('inf'):
            end_time = time.perf_counter()
            if return_details:
                return {
                    "path_found": None,
                    "exploration_order": exploration_order,
                    "explored_nodes_count": len(explored_nodes),
                    "processing_time_ms": round((end_time - start_time) * 1000, 4),
                }
            return None
        threshold = temp

#Build result
def build_result(meet, parent_start, parent_end, start, end):
    path = []
    cur = meet
    while cur != start:
        path.append(cur)
        cur = parent_start[cur]
    path.append(start)
    path.reverse()

    # If the meeting node is already the end node, the first half is complete.
    if meet == end:
        return path

    cur = parent_end[meet]
    while cur != end:
        path.append(cur)
        cur = parent_end[cur]
    path.append(end)

    return path


#BDS
def Bidirectional_bfs(grid, start, end):
    start_time = time.perf_counter()
    directions = [(0,-1), (-1,0), (0,1), (1,0)]
    n = len(grid)
    m = len(grid[0])

    if start == end:
        end_time = time.perf_counter()
        return {
            "path_found": [start],
            "exploration_order": [start],
            "explored_nodes_count": 1,
            "total_path_cost": 0,
            "max_queue_size": 1,
            "processing_time_us": (end_time - start_time) * 1000000
        }

    queue_start = deque([start])
    queue_end = deque([end])
    parent_start = {}
    parent_end = {}
    visited_start = set([start])
    visited_end = set([end])
    exploration_order = []
    queue_max_size = 2

    while queue_start and queue_end:

        for _ in range(len(queue_start)):
            x, y = queue_start.popleft()
            exploration_order.append((x, y))
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < m:
                    if grid[nx][ny] != 1 and (nx, ny) not in visited_start:
                        queue_start.append((nx,ny))
                        visited_start.add((nx,ny))
                        parent_start[(nx, ny)] = (x, y)
                        queue_max_size = max(queue_max_size, len(queue_end) + len(queue_start))
                        if (nx, ny) in visited_end:
                            path = build_result((nx,ny), parent_start, parent_end, start, end)
                            weighted_cost = calculate_path_cost(grid, path)
                            end_time = time.perf_counter()
                            return {
                                "path_found": path,
                                "exploration_order": exploration_order,
                                "explored_nodes_count": len(visited_end) + len(visited_start),
                                "total_path_cost": weighted_cost,
                                "max_queue_size": queue_max_size,
                                "processing_time_us": (end_time - start_time) * 1000000
                            }
        for _ in range(len(queue_end)):
            x, y = queue_end.popleft()
            exploration_order.append((x, y))
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < m:
                    if grid[nx][ny] != 1 and (nx, ny) not in visited_end:
                        queue_end.append((nx,ny))
                        visited_end.add((nx,ny))
                        parent_end[(nx, ny)] = (x, y)
                        queue_max_size = max(queue_max_size, len(queue_end) + len(queue_start))
                        if (nx, ny) in visited_start:
                            path = build_result((nx,ny), parent_start, parent_end, start, end)
                            weighted_cost = calculate_path_cost(grid, path)
                            end_time = time.perf_counter()
                            return {
                                "path_found": path,
                                "exploration_order": exploration_order,
                                "explored_nodes_count": len(visited_start) + len(visited_end),
                                "total_path_cost": weighted_cost,
                                "max_queue_size": queue_max_size,
                                "processing_time_us": (end_time - start_time) * 1000000
                            }
    end_time = time.perf_counter()
    return {
        "path_found": None,
        "exploration_order": exploration_order,
        "explored_nodes_count": len(visited_end) + len(visited_start),
        "total_path_cost": math.inf,
        "max_queue_size": queue_max_size,
        "processing_time_us": (end_time - start_time) * 1000000
    }


def get_cell_cost(cell_value):
    if cell_value == MONSTER_COST_VALUE:
        return MONSTER_COST_VALUE
    if cell_value == PLANT_COST_VALUE:
        return PLANT_COST_VALUE
    return 1


def calculate_path_cost(grid, path):
    if not path:
        return math.inf

    total_cost = 0
    for row, col in path[1:]:
        total_cost += get_cell_cost(grid[row][col])
    return total_cost

#DFS
def DFS(grid, start, end):
    start_time = time.perf_counter()
    directions = [(0,-1), (-1,0), (0,1), (1,0)]
    n = len(grid)
    m = len(grid[0])

    stack = [start]
    parent = {}
    visited = set([start])
    exploration_order = []
    stack_max_size = 1

    while stack:
        x,y  = stack.pop()
        exploration_order.append((x, y))

        if (x,y) == end:
            path = []
            cur = (x, y)
            while cur != start:
                path.append(cur)
                cur = parent[cur]
            path.append(start)
            path.reverse()
            weighted_cost = calculate_path_cost(grid, path)
            end_time = time.perf_counter()
            return {
                "path_found": path,
                "exploration_order": exploration_order,
                "explored_nodes_count": len(visited),
                "total_path_cost": weighted_cost,
                "max_queue_size": stack_max_size,
                "processing_time_us": (end_time - start_time) * 1000000
            }

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m:
                if grid[nx][ny] != 1 and (nx, ny) not in visited:
                    stack.append((nx,ny))
                    visited.add((nx,ny))
                    parent[(nx, ny)] = (x, y)
        stack_max_size = max(stack_max_size, len(stack))
    end_time = time.perf_counter()
    return {
        "path_found": None,
        "exploration_order": exploration_order,
        "explored_nodes_count": len(visited),
        "total_path_cost": math.inf,
        "max_queue_size": stack_max_size,
        "processing_time_us":(end_time - start_time) * 1000000
    }

"""
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
"""