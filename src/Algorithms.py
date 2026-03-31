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

def calculate_path_cost(grid, path):
    if not path:
        return None

    total_cost = 0
    for row, col in path[1:]:
        total_cost += get_cell_cost(grid[row][col])
    return total_cost

def Heuristic(node, goal):
    # Sử dụng Manhattan distance làm heuristic
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

#Uniform Cost Search (UCS)
def UCS(grid, start, goal):
    start_time = time.perf_counter()

    if not grid or not grid[0]:
        return {
            "path_found": None,
            "exploration_order": [],
            "explored_nodes_count": 0,
            "total_path_cost": math.inf,
            "max_queue_size": 0,
            "processing_time": 0,
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
                "processing_time": end_time - start_time,
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
        "processing_time": end_time - start_time,
    }

#A* Search
def A_search(grid, start, goal):
    start_time = time.perf_counter()

    if not grid or not grid[0]:
        return {
            "path_found": None,
            "exploration_order": [],
            "explored_nodes_count": 0,
            "total_path_cost": math.inf,
            "max_queue_size": 0,
            "processing_time": 0,
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
                "processing_time": end_time - start_time,
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
        "processing_time": end_time - start_time,
    }

#Jump Point Search (JPS)
def is_walkable(grid, node):
    rows, cols = len(grid), len(grid[0])
    r, c = node
    return 0 <= r < rows and 0 <= c < cols and grid[r][c] in WALKABLE_VALUES


def get_jump_directions(grid, current, parent):
    if parent is None:
        directions = []
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if is_walkable(grid, (current[0] + dr, current[1] + dc)):
                directions.append((dr, dc))
        return directions

    dr = current[0] - parent[0]
    dc = current[1] - parent[1]
    directions = []

    if dr != 0:
        if is_walkable(grid, (current[0] + dr, current[1])):
            directions.append((dr, 0))
        if is_walkable(grid, (current[0], current[1] + 1)) and not is_walkable(grid, (current[0] - dr, current[1] + 1)):
            directions.append((0, 1))
        if is_walkable(grid, (current[0], current[1] - 1)) and not is_walkable(grid, (current[0] - dr, current[1] - 1)):
            directions.append((0, -1))
    elif dc != 0:
        if is_walkable(grid, (current[0], current[1] + dc)):
            directions.append((0, dc))
        if is_walkable(grid, (current[0] + 1, current[1])) and not is_walkable(grid, (current[0] + 1, current[1] - dc)):
            directions.append((1, 0))
        if is_walkable(grid, (current[0] - 1, current[1])) and not is_walkable(grid, (current[0] - 1, current[1] - dc)):
            directions.append((-1, 0))

    return directions


def has_forced_neighbor(grid, node, direction):
    dx, dy = direction
    previous = (node[0] - dx, node[1] - dy)

    if dx != 0:
        if is_walkable(grid, (node[0], node[1] + 1)) and not is_walkable(grid, (previous[0], previous[1] + 1)):
            return True
        if is_walkable(grid, (node[0], node[1] - 1)) and not is_walkable(grid, (previous[0], previous[1] - 1)):
            return True
    elif dy != 0:
        if is_walkable(grid, (node[0] + 1, node[1])) and not is_walkable(grid, (previous[0] + 1, previous[1])):
            return True
        if is_walkable(grid, (node[0] - 1, node[1])) and not is_walkable(grid, (previous[0] - 1, previous[1])):
            return True

    return False


def jump(grid, current, direction, goal):
    next_node = (current[0] + direction[0], current[1] + direction[1])
    if not is_walkable(grid, next_node):
        return None
    if next_node == goal:
        return next_node
    if has_forced_neighbor(grid, next_node, direction):
        return next_node
    return jump(grid, next_node, direction, goal)


def expand_straight_line(current, jump_point):
    dr = 0 if jump_point[0] == current[0] else (1 if jump_point[0] > current[0] else -1)
    dc = 0 if jump_point[1] == current[1] else (1 if jump_point[1] > current[1] else -1)
    path = []
    node = current
    while node != jump_point:
        node = (node[0] + dr, node[1] + dc)
        path.append(node)
    return path


def Jump_Point_Search(grid, start, goal):
    start_time = time.perf_counter()
    if not grid or not grid[0]:
        return {
            "path_found": None,
            "exploration_order": [],
            "explored_nodes_count": 0,
            "total_path_cost": math.inf,
            "max_queue_size": 0,
            "processing_time": 0,
        }

    if start == goal:
        end_time = time.perf_counter()
        return {
            "path_found": [start],
            "exploration_order": [start],
            "explored_nodes_count": 1,
            "total_path_cost": 0,
            "max_queue_size": 1,
            "processing_time": end_time - start_time,
        }

    open_set = [(Heuristic(start, goal), 0, start, [start])]
    g_score = {start: 0}
    closed = set()
    exploration_order = []
    max_queue_size = 1

    while open_set:
        if len(open_set) > max_queue_size:
            max_queue_size = len(open_set)

        f_cost, current_g, current, path = heapq.heappop(open_set)
        if current in closed:
            continue

        closed.add(current)
        exploration_order.append(current)

        if current == goal:
            total_cost = calculate_path_cost(grid, path)
            end_time = time.perf_counter()
            return {
                "path_found": path,
                "exploration_order": exploration_order,
                "explored_nodes_count": len(closed),
                "total_path_cost": total_cost,
                "max_queue_size": max_queue_size,
                "processing_time": end_time - start_time,
            }

        parent = path[-2] if len(path) >= 2 else None
        for direction in get_jump_directions(grid, current, parent):
            jump_point = jump(grid, current, direction, goal)
            if jump_point is None or jump_point in closed:
                continue

            step_length = abs(jump_point[0] - current[0]) + abs(jump_point[1] - current[1])
            tentative_g = current_g + step_length
            if tentative_g >= g_score.get(jump_point, math.inf):
                continue

            g_score[jump_point] = tentative_g
            expanded_path = path + expand_straight_line(current, jump_point)
            heapq.heappush(open_set, (tentative_g + Heuristic(jump_point, goal), tentative_g, jump_point, expanded_path))

    end_time = time.perf_counter()
    return {
        "path_found": None,
        "exploration_order": exploration_order,
        "explored_nodes_count": len(closed),
        "total_path_cost": math.inf,
        "max_queue_size": max_queue_size,
        "processing_time": end_time - start_time,
    }

#Beam Search
def Beam_search(grid, start, goal, beam_width=2):
    start_time = time.perf_counter()

    if not grid or not grid[0]:
        return {
            "path_found": None,
            "exploration_order": [],
            "explored_nodes_count": 0,
            "total_path_cost": math.inf,
            "max_queue_size": 0,
            "processing_time": 0,
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
                    "processing_time": end_time - start_time,
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
        "processing_time": end_time - start_time,
    }


#IDA 
def dfs_search(matrix, start, goal, g, threshold, path, exploration_order, explored_nodes):
    current = path[-1]
    if current not in explored_nodes:
        explored_nodes.add(current)
        exploration_order.append(current)

    f = g + Heuristic(current, goal)
    if f > threshold:
        return f
    if current == goal:
        return True
    min_threshold = float('inf')
    for move in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        next_node = (current[0] + move[0], current[1] + move[1])
        if 0 <= next_node[0] < len(matrix) and 0 <= next_node[1] < len(matrix[0]) and next_node not in path:
            cell = matrix[next_node[0]][next_node[1]]
            if cell in WALKABLE_VALUES or next_node == goal:
                path.append(next_node)
                #Backtracking
                temp = dfs_search(matrix, start, goal, g + get_cell_cost(cell), threshold, path, exploration_order, explored_nodes)
                if temp == True:
                    return True
                if temp < min_threshold:
                    min_threshold = temp
                path.pop()
    return min_threshold

def ida_star(matrix, start, goal):
    start_time = time.perf_counter()
    threshold = Heuristic(start, goal)
    path = [start]
    exploration_order = []
    explored_nodes = set()

    while True:
        temp = dfs_search(matrix, start, goal, 0, threshold, path, exploration_order, explored_nodes)
        if temp == True:
            end_time = time.perf_counter()
            return {
                "path_found": path,
                "exploration_order": exploration_order,
                "explored_nodes_count": len(explored_nodes),
                "total_path_cost": calculate_path_cost(matrix, path),
                "max_queue_size": 0,
                "processing_time": end_time - start_time,
            }
        if temp == float('inf'):
            end_time = time.perf_counter()
            return {
                "path_found": None,
                "exploration_order": exploration_order,
                "explored_nodes_count": len(explored_nodes),
                "total_path_cost": math.inf,
                "max_queue_size": 0,
                "processing_time": end_time - start_time,
            }
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

#Bidirectional Search
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
            "processing_time": end_time - start_time
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
                    if grid[nx][ny] in WALKABLE_VALUES and (nx, ny) not in visited_start:
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
                                "explored_nodes_count": len(exploration_order),
                                "total_path_cost": weighted_cost,
                                "max_queue_size": queue_max_size,
                                "processing_time": end_time - start_time
                            }
        for _ in range(len(queue_end)):
            x, y = queue_end.popleft()
            exploration_order.append((x, y))
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < m:
                    if grid[nx][ny] in WALKABLE_VALUES and (nx, ny) not in visited_end:
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
                                "explored_nodes_count": len(exploration_order),
                                "total_path_cost": weighted_cost,
                                "max_queue_size": queue_max_size,
                                "processing_time": end_time - start_time
                            }
    end_time = time.perf_counter()
    return {
        "path_found": None,
        "exploration_order": exploration_order,
        "explored_nodes_count": len(exploration_order),
        "total_path_cost": math.inf,
        "max_queue_size": queue_max_size,
        "processing_time": end_time - start_time
    }

#Breadth-First Search (BFS)
def BFS(grid, start, goal):
    start_time = time.perf_counter()
    if not grid or not grid[0]:
        return {
            "path_found": None,
            "exploration_order": [],
            "explored_nodes_count": 0,
            "total_path_cost": math.inf,
            "max_queue_size": 0,
            "processing_time": 0,
        }

    rows, cols = len(grid), len(grid[0])
    if start == goal:
        end_time = time.perf_counter()
        return {
            "path_found": [start],
            "exploration_order": [start],
            "explored_nodes_count": 1,
            "total_path_cost": 0,
            "max_queue_size": 1,
            "processing_time": end_time - start_time,
        }

    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    queue = deque([start])
    visited = {start}
    parent = {}
    exploration_order = []
    max_queue_size = 1

    while queue:
        if len(queue) > max_queue_size:
            max_queue_size = len(queue)

        current = queue.popleft()
        exploration_order.append(current)

        if current == goal:
            path = []
            node = current
            while node != start:
                path.append(node)
                node = parent[node]
            path.append(start)
            path.reverse()
            total_cost = calculate_path_cost(grid, path)
            end_time = time.perf_counter()
            return {
                "path_found": path,
                "exploration_order": exploration_order,
                "explored_nodes_count": len(exploration_order),
                "total_path_cost": total_cost,
                "max_queue_size": max_queue_size,
                "processing_time": end_time - start_time,
            }

        for dr, dc in directions:
            neighbor = (current[0] + dr, current[1] + dc)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                neighbor_value = grid[neighbor[0]][neighbor[1]]
                if neighbor_value in WALKABLE_VALUES and neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

    end_time = time.perf_counter()
    return {
        "path_found": None,
        "exploration_order": exploration_order,
        "explored_nodes_count": len(exploration_order),
        "total_path_cost": math.inf,
        "max_queue_size": max_queue_size,
        "processing_time": end_time - start_time,
    }

#Depth-First Search (DFS)
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
                "explored_nodes_count": len(exploration_order),
                "total_path_cost": weighted_cost,
                "max_queue_size": stack_max_size,
                "processing_time": end_time - start_time
            }

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m:
                if grid[nx][ny] in WALKABLE_VALUES and (nx, ny) not in visited:
                    stack.append((nx,ny))
                    visited.add((nx,ny))
                    parent[(nx, ny)] = (x, y)
        stack_max_size = max(stack_max_size, len(stack))
    end_time = time.perf_counter()
    return {
        "path_found": None,
        "exploration_order": exploration_order,
        "explored_nodes_count": len(exploration_order),
        "total_path_cost": math.inf,
        "max_queue_size": stack_max_size,
        "processing_time":end_time - start_time
    }