import pygame
class Button:
    def __init__(self, x, y, w, h, img_normal, img_hover, img_pressed, onclick):
        self.rect = pygame.Rect(x, y, w, h)
        self.img_normal = img_normal
        self.img_hover = img_hover
        self.img_pressed = img_pressed
        self.is_pressed = False
        self.state = "normal"
        self.onclick = onclick

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        #Lấy vị trí con chuột và kiểm tra có nằm trong nút ko
        inside = self.rect.collidepoint(mouse_pos)

        if event.type == pygame.MOUSEMOTION:
            if self.is_pressed:
                return
            #Hover khi đưa con chuột vào nút
            self.state = "hover" if inside else "normal"

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if inside:
                self.is_pressed = True
                self.state = "pressed"
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            was_pressed = self.is_pressed
            self.is_pressed = False
            if was_pressed and inside:
                self.onclick()
            
            self.state = "hover" if inside else "normal"
    
    def draw(self, screen):
        if self.state == "normal":
            screen.blit(self.img_normal, self.rect)
        elif self.state == "hover":
            screen.blit(self.img_hover, self.rect)
        elif self.state == "pressed":
            screen.blit(self.img_pressed, self.rect)
