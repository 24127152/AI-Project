import pygame
from Button import Button
class Slider:
    def __init__(self, x, y, width, height, min_value=0, max_value=100, initial_value=50, on_apply=None):
        img_hover = pygame.image.load("assets/sprites/apply_hover.png")
        img_hover = pygame.transform.scale(img_hover, (20, 20))
        img_pressed = pygame.image.load("assets/sprites/apply_pressed.png")
        img_pressed = pygame.transform.scale(img_pressed, (20, 20))
        img_normal = pygame.image.load("assets/sprites/apply_normal.png")
        img_normal = pygame.transform.scale(img_normal, (20, 20))
        self.on_apply = on_apply
        self.apply_btn = Button(x + width + 13, y - 7, 40, 40, img_normal, img_hover, img_pressed, self.apply_value)

        self.rect = pygame.Rect(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = self._snap_to_odd(initial_value)
        self.handle_radius = height * 1.75

        #Màu nút trượt
        self.handle_color = (135, 206, 235)
        self.bar_color = (254, 255, 255)
        self.dragging = False

        fonts = pygame.font.Font("assets/fonts/Cyber.otf", 15)
        self.tile_text = fonts.render(f"Grid Size: {self.value} X {self.value}", True, (235, 245, 255))

    def _snap_to_odd(self, value):
        value = max(self.min_value, min(self.max_value, int(value)))
        if value % 2 == 1:
            return value

        #Cho phép tăng hoặc giảm 1 để đạt số lẻ
        if value + 1 <= self.max_value:
            return value + 1
        if value - 1 >= self.min_value:
            return value - 1
        return value

    def handle_event(self, event):
        self.apply_btn.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.update_value(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_value(event.pos[0])
    
    #Hàm cập nhật giá trị dựa trên vị trí chuột trene thanh trượt
    def update_value(self, mouse_x):
        relative_x = mouse_x - self.rect.x
        relative_x = max(0, min(relative_x, self.rect.width))
        raw_value = int((relative_x / self.rect.width) * (self.max_value - self.min_value) + self.min_value)
        self.value = self._snap_to_odd(raw_value)
        self.tile_text = pygame.font.Font("assets/fonts/Cyber.otf", 15).render(f"Grid Size: {self.value} X {self.value}", True, (235, 245, 255))
        
    #Hàm gọi apply khi nhấn nút apply
    def apply_value(self):
        if self.on_apply:
            self.on_apply(self._snap_to_odd(self.value))

    def draw(self, screen):
        self.apply_btn.draw(screen)
        #Vẽ thanh trượt
        screen.blit(self.tile_text, (self.rect.x + 20, self.rect.y - 25))
        pygame.draw.rect(screen, self.bar_color, self.rect)
        
        #Vị trí tay nắm trên thanh trượt
        handle_x = int((self.value - self.min_value) / (self.max_value - self.min_value) * self.rect.width) + self.rect.x
        
        #Vẽ tay nắm
        pygame.draw.circle(screen, self.handle_color, (handle_x, self.rect.centery), self.handle_radius)