import pygame
class Flag:
    def __init__(self, width, height):
        # Assuming you have a sprite sheet for the flag animation
        sheet = pygame.image.load("assets/sprites/flag.png").convert_alpha()
        #Điều chỉnh tỉ lệ
        sheet = pygame.transform.smoothscale(sheet, (width * 5, height))  
        frame_size = sheet.get_size()
        self.width = frame_size[0] // 5  # Assuming 5 frames horizontally
        self.height = frame_size[1]

        self.frames = []
        for index in range(5):
            frame_rect = pygame.Rect(index * self.width, 0, self.width, self.height)
            frame = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), frame_rect)
            self.frames.append(frame)

        self.current_frame = 0
        self.frame_duration_ms = 60
        self.last_tick = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_tick >= self.frame_duration_ms:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_tick = now

    def draw(self, screen, x, y):
        self.update()
        icon = self.frames[self.current_frame]
        rect = icon.get_rect(topleft=(x, y))
        screen.blit(icon, rect)

    def animate(self, screen, x, y):
        self.draw(screen, x, y)