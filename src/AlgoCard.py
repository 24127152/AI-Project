import pygame

class SpriteButton:
    def __init__(self, x, y, w, h, img_normal, img_hover, img_pressed):
        self.rect = pygame.Rect(x, y, w, h)
        self.image = img_normal
        self.img_normal = img_normal
        self.img_hover = img_hover
        self.img_pressed = img_pressed
        self.is_pressed = False
        self.state = "normal"

    def handle_event(self, event):
        #Lấy vị trí của chuột
        mouse_pos = pygame.mouse.get_pos()
        inside = self.rect.collidepoint(mouse_pos)
        clicked = False

        if event.type == pygame.MOUSEMOTION:
            if self.is_pressed:
                return False
            #Hover nếu di chuột vào nút
            self.state = "hover" if inside else "normal"
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if inside:
                self.is_pressed = True
                self.state = "pressed"

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            was_pressed = self.is_pressed
            self.is_pressed = False 
            
            if was_pressed and inside:
                clicked = True
            self.state = "hover" if inside else "normal"

        if self.state == "normal":
            self.image = self.img_normal
        elif self.state == "hover":
            self.image = self.img_hover
        elif self.state == "pressed":
            self.image = self.img_pressed

        return clicked

    def draw(self, screen):
        #Vẽ nút 
        screen.blit(self.image, self.rect)


class AlgoCard:
    def __init__(self):
        self.panel = pygame.image.load("assets/sprites/panel.png")
        self.panel = pygame.transform.scale(self.panel, (450, 150))

        #Vẽ nút bên trái
        left_img_normal = pygame.image.load("assets/sprites/left_arrow_normal.png")
        left_img_normal = pygame.transform.scale(left_img_normal, (45, 45))
        left_img_hover = pygame.image.load("assets/sprites/left_arrow_hover.png")
        left_img_hover = pygame.transform.scale(left_img_hover, (45, 45))
        left_img_pressed = pygame.image.load("assets/sprites/left_arrow_pressed.png")
        left_img_pressed = pygame.transform.scale(left_img_pressed, (45, 45))
        left = SpriteButton(420, 55, 50, 50, left_img_normal, left_img_hover, left_img_pressed)

        #Vẽ nút bên phải
        right_img_normal = pygame.image.load("assets/sprites/right_arrow_normal.png")
        right_img_normal = pygame.transform.scale(right_img_normal, (45, 45))
        right_img_hover = pygame.image.load("assets/sprites/right_arrow_hover.png")
        right_img_hover = pygame.transform.scale(right_img_hover, (45, 45))
        right_img_pressed = pygame.image.load("assets/sprites/right_arrow_pressed.png")
        right_img_pressed = pygame.transform.scale(right_img_pressed, (45, 45))
        right = SpriteButton(730, 55, 50, 50, right_img_normal, right_img_hover, right_img_pressed)

        #Tạo danh sách chứa các nút
        self.buttons = [left, right]
        self.current_index = 0
        self.algorithms = ["IDA*", "A*"]
        self.selected_algorithm = self.algorithms[self.current_index]

    def handle_event(self, event):
        #Trừ index đi 1 nếu nút trái
        if self.buttons[0].handle_event(event):
            self.current_index = (self.current_index - 1) % len(self.algorithms)
            self.selected_algorithm = self.algorithms[self.current_index]
            return self.selected_algorithm

        #Tăng index lên 1 nếu nút phải
        elif self.buttons[1].handle_event(event):
            self.current_index = (self.current_index + 1) % len(self.algorithms)
            self.selected_algorithm = self.algorithms[self.current_index]
            return self.selected_algorithm
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            return self.selected_algorithm

    def draw(self, screen):
        screen.blit(self.panel, (370, 0))
        for button in self.buttons:
            button.draw(screen)
        #vẽ tiêu đề và tên thuật toán đã chọn
        
        title_font = pygame.font.Font("assets/fonts/Cyber.otf", 22)
        title_font = title_font.render("Select Algorithm", True, (0, 0, 0))

        #Vẽ tên thuật toán đã chọn
        selection_text = pygame.font.Font("assets/fonts/Cyber.otf", 30)
        selection_text = selection_text.render(self.selected_algorithm, True, (0, 0, 0))
        screen.blit(selection_text,  (570, 62))
        screen.blit(title_font, (490, 9))