import pygame


class Earth:
    def __init__(self, width, height, screen_width, screen_height, margin=20):
        sheet = pygame.image.load("assets/sprites/earth.png").convert_alpha()
        frame_size = sheet.get_height()
        frame_count = sheet.get_width() // frame_size

        self.frames = []
        for index in range(frame_count):
            frame_rect = pygame.Rect(index * frame_size, 0, frame_size, frame_size)
            frame = pygame.Surface((frame_size, frame_size), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), frame_rect)
            frame = pygame.transform.smoothscale(frame, (width, height))
            self.frames.append(frame)

        self.current_frame = 0
        self.frame_duration_ms = 60
        self.last_tick = pygame.time.get_ticks()
        self.margin = margin
        self.anchor_x = screen_width - self.margin
        self.anchor_y = screen_height - self.margin

    def _update_frame(self):
        now = pygame.time.get_ticks()
        if now - self.last_tick >= self.frame_duration_ms:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_tick = now

    def animation(self, screen):
        #Vẽ hoạt ảnh trái đất
        self.draw(screen)

    def draw(self, screen):
        self._update_frame()
        icon = self.frames[self.current_frame]
        rect = icon.get_rect(bottomright=(self.anchor_x, self.anchor_y))
        screen.blit(icon, rect)