import pygame
from Flag import Flag

LEGEND_ASSETS = None

class Star:
    def __init__(self, width, height):
        self.base_width = width
        self.base_height = height
        self._load_frames(width, height)

    def _load_frames(self, width, height):
        sheet = pygame.image.load("assets/sprites/Star.png").convert_alpha()
        frames_count = 13

        frame_size = sheet.get_size()
        self.frames_width = frame_size[0] // frames_count
        self.frames_height = frame_size[1]
        self.frames = []
        for index in range(frames_count):
            frame_rect = pygame.Rect(index * frame_size[0] // frames_count, 0, frame_size[0] // frames_count, frame_size[1])
            frame = pygame.Surface((frame_size[0] // frames_count, frame_size[1]), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), frame_rect)
            self.frames.append(frame)

        self.current_frame = 0
        self.frame_duration_ms = 60
        self.last_tick = pygame.time.get_ticks()
    
    def update_size(self, width, height):
        #Cập nhật kích thước star
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
        rect = icon.get_rect(center=(x, y))
        screen.blit(icon, rect)


def _get_legend_assets():
    global LEGEND_ASSETS
    if LEGEND_ASSETS is not None:
        return LEGEND_ASSETS

    icon_size = (30, 30)
    start_node_sprite = Star(30, 30)
    

    wall_sprite = pygame.image.load("assets/sprites/meteor.png").convert_alpha()
    wall_sprite = pygame.transform.smoothscale(wall_sprite, icon_size)

    explored_surface = pygame.Surface(icon_size, pygame.SRCALPHA)
    explored_surface.fill((0, 0, 0, 0))
    pygame.draw.rect(explored_surface, (64, 196, 255), pygame.Rect(2, 2, 20, 20), border_radius=3)

    final_surface = pygame.Surface(icon_size, pygame.SRCALPHA)
    final_surface.fill((0, 0, 0, 0))
    pygame.draw.rect(final_surface, (255, 215, 0), pygame.Rect(2, 2, 20, 20), border_radius=4)

    
    font = pygame.font.Font("assets/fonts/Cyber.otf", 15)
    
    
    LEGEND_ASSETS = {
        "start_icon": start_node_sprite,
        "goal_icon": Flag(40, 40),
        "wall_icon": wall_sprite,
        "explored_icon": explored_surface,
        "final_icon": final_surface,
        "font": font,
    }
    return LEGEND_ASSETS


def draw_legend_panel(screen, x, y):
    assets = _get_legend_assets()
    #Vị trí và kích thước panel chú thích
    panel_rect = pygame.Rect(x - 250, y + 14, 700, 74)
    shadow_rect = panel_rect.move(0, 3)
    pygame.draw.rect(screen, (0, 0, 0, 90), shadow_rect, border_radius=12)
    pygame.draw.rect(screen, (12, 26, 42, 220), panel_rect, border_radius=12)
    pygame.draw.rect(screen, (76, 156, 199), panel_rect, 2, border_radius=12)
    
    #Danh sách chú thích và biểu tượng
    labels = (
        ("Start Node", assets["start_icon"]),
        ("Goal Node", assets["goal_icon"]),
        ("Wall", assets["wall_icon"]),
        ("Explored Path", assets["explored_icon"]),
        ("Final Path", assets["final_icon"]),
    )

    column_padding = 10
    content_width = panel_rect.width - (column_padding * 2)
    item_width = content_width / len(labels)

    for index, (label, icon) in enumerate(labels):
        cell_left = panel_rect.x + column_padding + (index * item_width)
        center_x = int(cell_left + item_width / 2)
        icon_center_y = panel_rect.y + 20
        text_y = panel_rect.y + 48

        if isinstance(icon, Flag):
            # Flag.draw dùng tọa độ topleft nên cần quy đổi từ tâm.
            frame = icon.frames[icon.current_frame]
            icon.draw(screen, center_x - frame.get_width() // 2, icon_center_y - frame.get_height() // 2)
        elif isinstance(icon, Star):
            icon.draw(screen, center_x, icon_center_y)
        else:
            rect = icon.get_rect(center=(center_x, icon_center_y))
            screen.blit(icon, rect)

        text_surface = assets["font"].render(label, True, (235, 245, 255))
        text_shadow = assets["font"].render(label, True, (8, 14, 24))
        text_rect = text_surface.get_rect(center=(center_x, text_y))
        shadow_rect = text_rect.move(1, 1)
        screen.blit(text_shadow, shadow_rect)
        screen.blit(text_surface, text_rect)