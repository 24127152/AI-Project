import pygame
class Maze:
    def __init__(self, width, height, image_path):
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (400, 400))

    def draw(self, screen):
        screen.blit(self.image, (300, 200))


