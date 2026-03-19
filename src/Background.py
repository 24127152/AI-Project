import pygame
class Background:
    def __init__(self, width, height, image_path):
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (1000, 800))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))