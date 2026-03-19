import pygame 
class Maze:
    def __init__(self, width, height, image_path):
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (400, 400))

    def draw(self, screen):
        screen.blit(self.image, (300, 200))

class Background:
    def __init__(self, width, height, image_path):
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (1000, 800))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

if __name__ == "__main__":

    nature_sound = pygame.mixer.Sound("assets/nature_sound.wav")
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    maze = Maze(500, 500, "assets/maze.png")
    background = Background(1000, 800, "assets/background.jpg")
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        background.draw(screen)
        maze.draw(screen)
        pygame.display.flip()

    # Giống return 0 trong c++
    pygame.quit()
    
