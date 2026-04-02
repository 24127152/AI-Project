import pygame

class Bot:
    def __init__(self, image_path, path, node_width, node_height):
        # 1. Tối ưu tỷ lệ: Bot chiếm 75% chiều rộng và 85% chiều cao của ô
        # Giảm mức giới hạn (floor) xuống 6px để bot có thể co lại cực nhỏ cho map khổng lồ
        self.draw_width = max(6, int(node_width * 1))
        self.draw_height = max(8, int(node_height * 1))
        
        self.bot_x = 0
        self.bot_y = 0

        self.node_width = node_width
        self.node_height = node_height

        self.path = path if path is not None else []
        self.path_index = 0
        
        # 2. Tốc độ động: Tốc độ bằng 1/3 kích thước ô, thấp nhất là 2px/frame
        self.speed = max(1.5, node_width // 3)

        self.animate = pygame.image.load("assets/sprites/bot_animate.png").convert_alpha()
        self.is_moving = False
        self.frame_width = self.animate.get_width() // 7
        self.frame_height = self.animate.get_height()
        self.frame_count = max(1, self.animate.get_width() // self.frame_width)
        self.frames = []
        for i in range(self.frame_count):
            frame = self.animate.subsurface((i * self.frame_width, 0, self.frame_width, self.frame_height)).copy()

            # Loại bỏ phần trong suốt xung quanh bot để tránh vẽ những pixel thừa khi di chuyển
            content_rect = frame.get_bounding_rect(min_alpha=1)
            if content_rect.width > 0 and content_rect.height > 0:
                frame = frame.subsurface(content_rect).copy()

            frame = pygame.transform.scale(frame, (self.draw_width, self.draw_height))
            self.frames.append(frame)

        self.idle_sheet = pygame.image.load("assets/sprites/bot_idle.png").convert_alpha()

        self.idle_frames = []
        self.frame_idle_width = self.idle_sheet.get_width() // 7
        self.frame_idle_height = self.idle_sheet.get_height()
        self.frame_idle_count = max(1, self.idle_sheet.get_width() // self.frame_idle_width)
        for i in range(self.frame_idle_count):
            frame = self.idle_sheet.subsurface((i * self.frame_idle_width, 0, self.frame_idle_width, self.frame_idle_height)).copy()
            content_rect = frame.get_bounding_rect(min_alpha=1)
            if content_rect.width > 0 and content_rect.height > 0:
                frame = frame.subsurface(content_rect).copy()
            frame = pygame.transform.scale(frame, (self.draw_width, self.draw_height))
            self.idle_frames.append(frame)

        self.current_frame = 0
        self.idle_frame_index = 0
        self.frame_duration_ms = 60
        self.idle_frame_duration_ms = 120
        self.last_tick = pygame.time.get_ticks()
        self.last_idle_tick = pygame.time.get_ticks()
        self.has_animation = len(self.frames) > 1
        self.has_idle_animation = len(self.idle_frames) > 0

    def draw(self, screen):
        if self.is_moving and self.has_animation:
            screen.blit(self.frames[self.current_frame], (self.bot_x, self.bot_y))
        else:
            self.idle_animation()
            if self.has_idle_animation:
                screen.blit(self.idle_frames[self.idle_frame_index], (self.bot_x, self.bot_y))

    def set_position(self, x, y):
        # 3. Căn giữa khi vừa được đặt vào game
        center_offset_x = (self.node_width - self.draw_width) // 2
        center_offset_y = (self.node_height - self.draw_height) // 2
        self.bot_x = x + center_offset_x
        self.bot_y = y + center_offset_y
    
    def update(self, x, y, matrix, maze_shift_x=0):
        W = len(matrix[0]) * self.node_width
        H = len(matrix) * self.node_height
        offset_x = (x - W) // 2 + maze_shift_x
        offset_y = (y - H) // 2
        moved = False
        
        if self.path and self.path_index < len(self.path):
            row, col = self.path[self.path_index]
            
            # 3. Căn giữa tọa độ đích cho mỗi bước đi
            target_x = offset_x + col * self.node_width + (self.node_width - self.draw_width) // 2
            target_y = offset_y + row * self.node_height + (self.node_height - self.draw_height) // 2
            
            if self.bot_x < target_x:
                self.bot_x += self.speed
                moved = True
            elif self.bot_x > target_x:
                self.bot_x -= self.speed
                moved = True
                
            if self.bot_y < target_y:
                self.bot_y += self.speed
                moved = True
            elif self.bot_y > target_y:
                self.bot_y -= self.speed
                moved = True
                
            # Kiểm tra xem đã đến đúng đích (cho phép sai số bằng tốc độ)
            if abs(self.bot_x - target_x) <= self.speed and abs(self.bot_y - target_y) <= self.speed:
                self.bot_x = target_x
                self.bot_y = target_y   
                self.path_index += 1
        
        self.is_moving = moved
        if self.is_moving:
            self.animation()
        elif not self.path or self.path_index >= len(self.path):
            self.current_frame = 0
            self.idle_animation()

    def animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_tick >= self.frame_duration_ms:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_tick = now

    def idle_animation(self):
        if not self.idle_frames:
            return
        now = pygame.time.get_ticks()
        if now - self.last_idle_tick >= self.idle_frame_duration_ms:
            self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_frames)
            self.last_idle_tick = now