import pygame
class StatsPanel:
    def __init__(self):
        self.stats = {
            "Algorithm": "N/A",
            "Result": "N/A",
            "Path length": "N/A",
            "Time": "N/A"
        }
        self.image = pygame.image.load("assets/sprites/stats_panel.png")
        self.image = pygame.transform.scale(self.image, (350, 270))

    def update_stats(self, algorithm, result, path_length, execution_time):
        self.stats["Algorithm"] = algorithm
        self.stats["Result"] = result
        self.stats["Path length"] = path_length
        self.stats["Time"] = f"{execution_time:4f} sec" if execution_time is not None else "N/A"

    def draw(self, screen):
        #Điều chỉnh kích thước chữ
        font = pygame.font.Font("assets/fonts/Cyber.otf", 20)
        tile_font = pygame.font.Font("assets/fonts/Cyber.otf", 30)
        y_offset = 30
        screen.blit(self.image, (-10, -10))
        title_surface = tile_font.render("Status", True, (224, 255, 255))
        screen.blit(title_surface, (20, y_offset - 10))
        for key, value in self.stats.items():
            text = f"{key}: {value}"
            text_surface = font.render(text, True, (224, 255, 255))
            screen.blit(text_surface, (20, y_offset + 40))
            y_offset += 35

    
