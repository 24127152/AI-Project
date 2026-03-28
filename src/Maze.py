import pygame
from Tile import Tile
from Bot import Bot
import random
tile_size = 30
tile = Tile(30, 30, "assets/sprites/meteor.png")

class Maze:

    def __init__(self, width, height, image_path):
        self.width = width
        self.height = height
        self.node_width = 30
        self.node_height = 30

    def load_matrix(self, file_path):
        #Đọc file Matrix.txt và vẽ ma trận bằng tile
        with open(file_path, "r") as file:
            matrix = []
            for line in file:
                row = list(map(int, line.split()))
                matrix.append(row)
        return matrix
    
    def generate_maze(self, size):
        """Tạo maze ngẫu nhiên với kích thước size x size, đảm bảo có đường từ start tới goal"""
        size = max(5, int(size))
        if size % 2 == 0:
            size -= 1

        matrix = [[1 for _ in range(size)] for _ in range(size)]
        
        # Tạo đường đi ngẫu nhiên bằng carving path
        visited = [[False for _ in range(size)] for _ in range(size)]
        
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
        
        # Đảm bảo có đường từ cửa vào tới cửa ra (hành lang chữ L)
        for j in range(1, size - 1):
            matrix[1][j] = 0
        for i in range(1, size - 1):
            matrix[i][size - 2] = 0

        # Cửa vào bên trái và cửa ra bên phải
        matrix[1][0] = 2
        matrix[size - 2][size - 1] = 3

        # Mở ô ngay trong cửa để nhân vật đi vào/ra
        matrix[1][1] = 0
        matrix[size - 2][size - 2] = 0
        
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
        
