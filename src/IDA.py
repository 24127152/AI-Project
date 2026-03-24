import pygame
import time

MONSTER_COST_VALUE = 5
PLANT_COST_VALUE = 6


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