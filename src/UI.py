import pygame 
from Maze import Maze
from Background import Background

class Bot:
    def __init__(self, width, height, image_path):
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)

    def draw(self, screen):
        screen.blit(self.image, (0, 0))


if __name__ == "__main__":

    
    pygame.init()
    #Âm thanh nền
    nature_sound = pygame.mixer.Sound("assets/sounds/nature_sound.wav")
    nature_sound.play(-1)  # Phát âm thanh lặp lại

    screen = pygame.display.set_mode((1000, 800))
    maze = Maze(500, 500, "assets/sprites/maze.png")
    background = Background(1000, 800, "assets/sprites/background.jpg")
    bot = Bot(50, 50, "assets/sprites/bot.png")
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        background.draw(screen)
        maze.draw(screen)
        bot.draw(screen)
        pygame.display.flip()

    # Giống return 0 trong c++
    pygame.quit()
    
