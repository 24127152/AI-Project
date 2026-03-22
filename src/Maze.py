import pygame
from Tile import Tile
from Bot import Bot
tile_size = 30
tile = Tile(30, 30, "assets/sprites/meteor.png")
#tile.image = pygame.transform.scale(tile.image, (96, 96))
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

    def draw_maze(self, matrix, screen, x, y, bot):
        #Tính toán vị trí để vẽ mê cung
        W = len(matrix[0]) * tile_size
        H = len(matrix) * tile_size
        offset_x = (x - W) // 2
        offset_y = (y - H) // 2

        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                if value == 1:
                    tile_x = offset_x + j * tile_size
                    tile_y = offset_y + i * tile_size
                    tile.draw(screen, tile_x, tile_y)
                

    def find_pos(self, matrix, start, goal, bot, x, y):
        #Vị trí chính xác của bot
        W = len(matrix[0]) * tile_size
        H = len(matrix) * tile_size
        offset_x = (x - W) // 2
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
        
