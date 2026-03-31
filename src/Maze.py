import pygame
from Tile import Tile
from Bot import Bot
import random

# Đã thu nhỏ kích thước tile từ 30 xuống 15 để chứa được mê cung lớn
tile_size = 15
tile = Tile(15, 15, "assets/sprites/meteor.png")

class Maze:

    def __init__(self, width, height, image_path):
        self.width = width
        self.height = height
        # Đồng bộ kích thước node với tile_size
        self.node_width = 15
        self.node_height = 15

    def load_matrix(self, file_path):
        #Đọc file Matrix.txt và vẽ ma trận bằng tile
        with open(file_path, "r") as file:
            matrix = []
            for line in file:
                row = list(map(int, line.split()))
                matrix.append(row)
        return matrix
    
    def generate_maze(self, size):
        """Tạo Braid Maze (Mê cung bện) siêu khó, đan xen nhiều đường, random start/goal xa nhau"""
        size = max(5, int(size))
        if size % 2 == 0:
            size -= 1

        matrix = [[1 for _ in range(size)] for _ in range(size)]
        visited = [[False for _ in range(size)] for _ in range(size)]
        
        # 1. Thuật toán Carving path tạo cấu trúc mê cung cơ bản với nhiều ngõ cụt
        def carve_path(x, y):
            visited[y][x] = True
            matrix[y][x] = 0
            
            directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < size and 0 <= ny < size and not visited[ny][nx]:
                    matrix[y + dy//2][x + dx//2] = 0
                    carve_path(nx, ny)
        
        carve_path(1, 1)

        # 2. THUẬT TOÁN BRAID: Khử ngõ cụt để tạo vô số đường vòng phức tạp
        dead_ends = []
        for y in range(1, size - 1):
            for x in range(1, size - 1):
                if matrix[y][x] == 0:
                    walls = 0
                    if matrix[y-1][x] == 1: walls += 1
                    if matrix[y+1][x] == 1: walls += 1
                    if matrix[y][x-1] == 1: walls += 1
                    if matrix[y][x+1] == 1: walls += 1
                    
                    if walls == 3: # Đây là 1 ngõ cụt
                        dead_ends.append((x, y))

        # Phá khoảng 75% ngõ cụt để nối với các đường khác
        # Cố tình giữ lại 25% ngõ cụt để làm "bẫy" đánh lừa các thuật toán
        braid_ratio = 0.75 
        random.shuffle(dead_ends)
        braid_count = int(len(dead_ends) * braid_ratio)

        for i in range(braid_count):
            x, y = dead_ends[i]
            # Chọn tường xung quanh ngõ cụt để đập (tránh viền ngoài cùng)
            possible_walls = []
            if matrix[y-1][x] == 1 and y-1 > 0: possible_walls.append((x, y-1))
            if matrix[y+1][x] == 1 and y+1 < size-1: possible_walls.append((x, y+1))
            if matrix[y][x-1] == 1 and x-1 > 0: possible_walls.append((x-1, y))
            if matrix[y][x+1] == 1 and x+1 < size-1: possible_walls.append((x+1, y))

            if possible_walls:
                wx, wy = random.choice(possible_walls)
                matrix[wy][wx] = 0 # Nối ngõ cụt sang đường bên cạnh

        # 3. Random vị trí Cửa Vào (2) và Cửa Ra (3) với khoảng cách xa nhau
        valid_starts = []
        valid_goals = []
        
        for i in range(1, size - 1):
            if matrix[1][i] == 0: valid_starts.append((0, i))
            if matrix[size-2][i] == 0: valid_goals.append((size-1, i))
            if matrix[i][1] == 0: valid_starts.append((i, 0))
            if matrix[i][size-2] == 0: valid_goals.append((i, size-1))

        if not valid_starts: valid_starts = [(0, 1)]
        if not valid_goals: valid_goals = [(size-1, size-2)]

        start_pos = random.choice(valid_starts)
        matrix[start_pos[0]][start_pos[1]] = 2
        
        def manhattan_distance(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

        # Bắt buộc Goal phải cách Start ít nhất 70% kích thước mê cung
        min_distance = int(size * 0.7) 
        far_goals = [pos for pos in valid_goals if manhattan_distance(start_pos, pos) >= min_distance]
        
        if far_goals:
            goal_pos = random.choice(far_goals)
        else:
            valid_goals = [pos for pos in valid_goals if pos != start_pos]
            if valid_goals:
                goal_pos = max(valid_goals, key=lambda p: manhattan_distance(start_pos, p))
            else:
                goal_pos = (size-1, size-2)
                
        matrix[goal_pos[0]][goal_pos[1]] = 3
        
        return matrix

    def draw_maze(self, matrix, screen, x, y, bot, maze_shift_x=0):
        #Tính toán vị trí để vẽ mê cung
        W = len(matrix[0]) * tile_size
        H = len(matrix) * tile_size
        offset_x = (x - W) // 2 + maze_shift_x
        offset_y = (y - H) // 2

        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                if value == 1:
                    tile_x = offset_x + j * tile_size
                    tile_y = offset_y + i * tile_size
                    tile.draw(screen, tile_x, tile_y)
                

    def find_pos(self, matrix, start, goal, bot, x, y, maze_shift_x=0):
        #Vị trí chính xác của bot
        W = len(matrix[0]) * tile_size
        H = len(matrix) * tile_size
        offset_x = (x - W) // 2 + maze_shift_x
        offset_y = (y - H) // 2
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                if value == 2:
                    start = (i, j)
                    x = offset_x +  start[1] * self.node_width
                    y = offset_y + start[0] * self.node_height
                    bot.set_position(x, y)
                elif value == 3:
                    goal = (i, j)
        return start, goal