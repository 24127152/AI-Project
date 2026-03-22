import pygame
class Tile:
    def __init__(self, width, heigth, image_path):
        self.width = width
        self.height = heigth
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))