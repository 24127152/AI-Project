import pygame
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])



def dfs_search(matrix, start, goal, g, threshold, path):
    current = path[-1]
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
            if cell == 0 or next_node == goal:
                path.append(next_node)
                #Backtracking
                temp = dfs_search(matrix, start, goal, g + 1, threshold, path)
                if temp == True:
                    return True
                if temp < min_threshold:
                    min_threshold = temp
                path.pop()
    return min_threshold

def ida_star(matrix, start, goal):
    threshold = heuristic(start, goal)
    path = [start]
    while True:
        temp = dfs_search(matrix, start, goal, 0, threshold, path)
        if temp == True:
            return path
        if temp == float('inf'):
            return None
        threshold = temp