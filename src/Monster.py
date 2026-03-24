import pygame

class Monster:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 0, 0)  # Màu đỏ cho quái vật

        self.sheet = pygame.image.load("assets/sprites/SlimeA.png").convert_alpha()
        self.sheet = pygame.transform.smoothscale(self.sheet, (width * 16, height))  # Điều chỉnh tỉ lệ sprite sheet
        self.frames = []
        self.frame_width = self.sheet.get_width() // 16  # Giả sử có 16 khung hình trong sprite sheet
        self.frame_height = self.sheet.get_height()
        self.frame_count = max(1, self.sheet.get_width() // self.frame_width)
        
        
        for i in range(self.frame_count):
            frame = self.sheet.subsurface((i * self.frame_width, 0, self.frame_width, self.frame_height)).copy()
            self.frames.append(frame)

        self.current_frame = 0
        self.frame_duration_ms = 80
        self.last_tick = pygame.time.get_ticks()

    def draw(self, screen):
        self.update()
        icon = self.frames[self.current_frame]
        rect = icon.get_rect(topleft=(self.rect.x, self.rect.y))
        screen.blit(icon, rect)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_tick >= self.frame_duration_ms:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_tick = now