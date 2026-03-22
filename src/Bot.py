import pygame
tile_size = 30
class Bot:
    def __init__(self, image_path, path, node_width, node_height):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (25, 30))
        self.bot_x = 0
        self.bot_y = 0

        self.node_width = node_width
        self.node_height = node_height

        self.path = path if path is not None else []
        self.path_index = 0
        #Speed để bot di từ từ
        self.speed = 1.0

    def draw(self, screen):
        screen.blit(self.image, (self.bot_x, self.bot_y))

    def set_position(self, x, y):
        self.bot_x = x
        self.bot_y = y
    
    def update(self,x , y, matrix):
        W = len(matrix[0]) * tile_size
        H = len(matrix) * tile_size
        offset_x = (x - W) // 2
        offset_y = (y - H) // 2
        
        if self.path and self.path_index < len(self.path):
            row, col = self.path[self.path_index]
            x = offset_x + col * self.node_width
            y = offset_y + row * self.node_height
            if self.bot_x < x:
                self.bot_x += self.speed
            elif self.bot_x > x:
                self.bot_x -= self.speed
            if self.bot_y < y:
                self.bot_y += self.speed
            elif self.bot_y > y:
                self.bot_y -= self.speed
            if abs(self.bot_x - x) < self.speed and abs(self.bot_y - y) < self.speed:
                self.bot_x = x
                self.bot_y = y   
                self.path_index += 1
