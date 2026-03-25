import pygame
import os
import math # Thêm thư viện toán học để tạo hiệu ứng dao động
from Button import Button
# Hàm load ảnh an toàn
def load_img_safe(path, size, fallback_color=(150, 0, 150)):
    if os.path.exists(path):
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    else:
        surf = pygame.Surface(size)
        surf.fill(fallback_color)
        return surf

class MainMenu:
    def __init__(self, width, height, cb_play, cb_quit):
        self.width = width
        self.height = height
        
        try:
            self.title_font = pygame.font.Font("assets/fonts/Cyber.otf", 80)
        except:
            self.title_font = pygame.font.SysFont(None, 80)
        
        # Nút Play ở y=350
        self.btn_play = Button(500, 350, 200, 60, 
                               load_img_safe("assets/sprites/play_normal.png", (200, 60)), 
                               load_img_safe("assets/sprites/play_hover.png", (200, 60)), 
                               load_img_safe("assets/sprites/play_pressed.png", (200, 60)), onclick=cb_play)
        
        # Nút Quit ở y=450
        self.btn_quit = Button(500, 450, 200, 60, 
                               load_img_safe("assets/sprites/quit_normal.png", (200, 60)), 
                               load_img_safe("assets/sprites/quit_hover.png", (200, 60)), 
                               load_img_safe("assets/sprites/quit_pressed.png", (200, 60)), onclick=cb_quit)

    def handle_event(self, event):
        self.btn_play.handle_event(event)
        self.btn_quit.handle_event(event)

    def draw(self, screen):
        title_text = self.title_font.render("MAZE SOLVER", True, (255, 255, 255))
        
        # --- HIỆU ỨNG BAY BỔNG (FLOATING ANIMATION) ---
        # Lấy thời gian thực của game đang chạy (tính bằng mili-giây)
        current_time = pygame.time.get_ticks() 
        
        # Hàm sin tạo ra giá trị nhịp nhàng từ -1 đến 1. 
        # Nhân thời gian với 0.003 để chữ trôi từ từ (tốc độ dao động).
        # Nhân tất cả với 15 để chữ nảy lên/xuống tối đa 15 pixel (biên độ).
        offset_y = math.sin(current_time * 0.003) * 15 
        
        # Tọa độ Y gốc của chữ là 120, giờ cộng thêm độ lệch offset_y
        title_y = 120 + offset_y 
        # ----------------------------------------------
        
        # Vẽ chữ ra màn hình với tọa độ Y đã được tính toán lại liên tục
        screen.blit(title_text, (self.width//2 - title_text.get_width()//2, title_y))
        
        self.btn_play.draw(screen)
        self.btn_quit.draw(screen)