import pygame
class Flag:
    def __init__(self, width, height):
        #Sprites hoạt họa cờ
        sheet = pygame.image.load("assets/sprites/flag.png").convert_alpha()
        self.base_width = width
        self.base_height = height
        self._load_frames(width, height)

    def _load_frames(self, width, height):
        sheet = pygame.image.load("assets/sprites/flag.png").convert_alpha()
        #Điều chỉnh tỉ lệ
        sheet = pygame.transform.smoothscale(sheet, (width * 5, height))  
        frame_size = sheet.get_size()
        #5 sprites hoạt họa 
        self.width = frame_size[0] // 5  
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
    
    def update_size(self, width, height):
        #Cập nhật kích thước flag
        self.base_width = width
        self.base_height = height
        self._load_frames(width, height)

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