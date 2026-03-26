import pygame
import os
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
        base_size = min(self.width, self.height)

        #Baren
        self.baren = self._load_and_scale_planet("assets/Planets/Baren.png", (int(base_size * 0.34), int(base_size * 0.34)))
        #Black hole
        self.black_hole = self._load_and_scale_planet("assets/Planets/Black_hole.png", (int(base_size * 0.26), int(base_size * 0.26)))

        #ice
        self.ice = self._load_and_scale_planet("assets/Planets/Ice.png", (int(base_size * 0.24), int(base_size * 0.24)))

        #Lava
        self.lava = self._load_and_scale_planet("assets/Planets/Lava.png", (int(base_size * 0.30), int(base_size * 0.30)))

        #Terran
        self.teran = self._load_and_scale_planet("assets/Planets/Terran.png", (int(base_size * 0.27), int(base_size * 0.27)))

        # Bố cục hành tinh theo viền màn hình để giữ vùng trung tâm thoáng cho logo và nút.
        self.planet_positions = {
            "baren": (-int(base_size * 0.08), int(self.height * 0.06)),
            "black_hole": (self.width - self.black_hole.get_width() + int(base_size * 0.05), -int(base_size * 0.05)),
            "ice": (int(self.width * 0.04), self.height - self.ice.get_height() + int(base_size * 0.06)),
            "lava": (self.width - self.lava.get_width() - int(self.width * 0.03), self.height - self.lava.get_height() - int(self.height * 0.04)),
            "teran": (self.width - self.teran.get_width() - int(self.width * 0.18), int(self.height * 0.18)),
        }

        self.logo = pygame.image.load("assets/sprites/logo.png").convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (300, 300))
        self.button_width = 200
        self.button_height = 60
        button_x = (self.width - self.button_width) // 2
        
        try:
            self.title_font = pygame.font.Font("assets/fonts/Cyber.otf", 80)
        except:
            self.title_font = pygame.font.SysFont(None, 80)
        
        # Nút Play ở y=350
        self.btn_play = Button(button_x, 350, self.button_width, self.button_height, 
                       load_img_safe("assets/sprites/play_normal.png", (self.button_width, self.button_height)), 
                       load_img_safe("assets/sprites/play_hover.png", (self.button_width, self.button_height)), 
                       load_img_safe("assets/sprites/play_pressed.png", (self.button_width, self.button_height)), onclick=cb_play)
        
        # Nút Quit ở y=450
        self.btn_quit = Button(button_x, 450, self.button_width, self.button_height, 
                       load_img_safe("assets/sprites/quit_normal.png", (self.button_width, self.button_height)), 
                       load_img_safe("assets/sprites/quit_hover.png", (self.button_width, self.button_height)), 
                       load_img_safe("assets/sprites/quit_pressed.png", (self.button_width, self.button_height)), onclick=cb_quit)

    def _load_and_scale_planet(self, path, size):
        return load_img_safe(path, size)

    def handle_event(self, event):
        self.btn_play.handle_event(event)
        self.btn_quit.handle_event(event)

    def draw(self, screen):
        #Vẽ nền với các hình ảnh khác nhau
        screen.blit(self.black_hole, self.planet_positions["black_hole"])
        screen.blit(self.baren, self.planet_positions["baren"])
        screen.blit(self.teran, self.planet_positions["teran"])
        screen.blit(self.ice, self.planet_positions["ice"])
        screen.blit(self.lava, self.planet_positions["lava"])

        #vẽ logo ở giữa 
        logo_rect = self.logo.get_rect(center=(self.width//2, 250))
        screen.blit(self.logo, logo_rect)

        title_text = self.title_font.render("MAZE SOLVER", True, (255, 255, 255))

        # Vẽ chữ tĩnh, không hiệu ứng dao động.
        screen.blit(title_text, (self.width//2 - title_text.get_width()//2, 120))
        
        self.btn_play.draw(screen)
        self.btn_quit.draw(screen)