import time
import math
from collections import deque

MONSTER_COST_VALUE = 5
PLANT_COST_VALUE = 6
"""
with open("Matrix.txt", "r") as fi:
    grid = []
    start = end = None
    for i,line in enumerate(fi):
        if line.strip() == "":
            continue
        row = list(map(int, line.split()))
        grid.append(row)

        for j, val in enumerate(row):
            if val == 2:
                start = (i, j)
            elif val == 3:
                end = (i, j)

"""


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

"""
result = DFS(grid, start, end)

print("Path:", result["path_found"])
print("Cost:", result["total_path_cost"])
print("Explored nodes:", result["explored_nodes_count"])
print("Max stack size:", result["max_queue_size"])
print("Time (uys):", result["processing_time_us"])

result = Bidirectional_bfs(grid, start, end)

print("Path:", result["path_found"])
print("Cost:", result["total_path_cost"])
print("Explored nodes:", result["explored_nodes_count"])
print("Max stack size:", result["max_queue_size"])
print("Time (us):", result["processing_time_us"])
"""

