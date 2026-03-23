import pygame
class Slider:
    def __init__(self, x, y, width, height, min_value=0, max_value=100, initial_value=50):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.handle_radius = height * 1.5
        self.handle_color = (200, 200, 200)
        self.bar_color = (254, 255, 255)
        self.dragging = False

        fonts = pygame.font.Font("assets/fonts/Cyber.otf", 15)
        self.tile_text = fonts.render(f"Grid Size: {self.value} X {self.value}", True, (235, 245, 255))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.update_value(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_value(event.pos[0])

    def update_value(self, mouse_x):
        relative_x = mouse_x - self.rect.x
        relative_x = max(0, min(relative_x, self.rect.width))
        self.value = int((relative_x / self.rect.width) * (self.max_value - self.min_value) + self.min_value)
        self.tile_text = pygame.font.Font("assets/fonts/Cyber.otf", 15).render(f"Grid Size: {self.value} X {self.value}", True, (235, 245, 255))

    def draw(self, screen):
        # Draw the bar
    
        screen.blit(self.tile_text, (self.rect.x + 10, self.rect.y - 25))
        pygame.draw.rect(screen, self.bar_color, self.rect)
        
        # Calculate handle position
        handle_x = int((self.value - self.min_value) / (self.max_value - self.min_value) * self.rect.width) + self.rect.x
        
        # Draw the handle
        pygame.draw.circle(screen, self.handle_color, (handle_x, self.rect.centery), self.handle_radius)