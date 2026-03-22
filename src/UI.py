import pygame 
from Maze import Maze
from Background import Background
from Bot import Bot
from IDA import ida_star
from Button import Button
from AlgoCard import AlgoCard
from StatsPanel import StatsPanel
from Earth import Earth
import time

#Hàm vẽ dường đi
def draw_path_progression(screen, matrix, path, progress_index, width, height, tile_size):
    if not path:
        return

    W = len(matrix[0]) * tile_size
    H = len(matrix) * tile_size
    offset_x = (width - W) // 2
    offset_y = (height - H) // 2

    last = min(progress_index, len(path) - 1)
    for k in range(last + 1):
        i, j = path[k]
        x = offset_x + j * (tile_size) + tile_size // 2 - 5
        y = offset_y  + i * (tile_size) + tile_size // 2 - 5
        pygame.draw.rect(screen, (255, 215, 0), (x, y, 10, 10))

if __name__ == "__main__":

    WIDTH = 1200
    HEIGHT = 800
    pygame.init()
    #Âm thanh nền
    nature_sound = pygame.mixer.Sound("assets/sounds/nature_sound.wav")
    nature_sound.play(-1)  # Phát âm thanh lặp lại

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    maze = Maze(500, 500, "assets/sprites/maze.png")
    matrix  = maze.load_matrix("src/Matrix.txt")

    background = Background(WIDTH, HEIGHT, "assets/sprites/Background.png")

    stats_panel = StatsPanel()
    path = []
    
    #Tạo bot
    bot = Bot("assets/sprites/bot.png", path, maze.node_width, maze.node_height)
    start, goal = maze.find_pos(matrix, (0, 0), (len(matrix) - 1, len(matrix[0]) - 1), bot, WIDTH, HEIGHT)
    running = True
    algorithm_running = False
    def start_algorithm():
        global algorithm_running, path, time_taken, algorithm_complete
         
        if not algorithm_running:
            start_perf = time.perf_counter()
            path = ida_star(matrix, start, goal) or []
            end_time = time.perf_counter()
            time_taken = end_time - start_perf
            bot.path = path
            bot.path_index = 0
            algorithm_running = True

        algorithm_complete = True
        
            
    #Reset thuật toán
    def restart_algorithm():
        global algorithm_running, path, time_taken, bot
        path = []
        bot.path = path
        bot.path_index = 0
        algorithm_running = False
        time_taken = None
        offset_x = (WIDTH - len(matrix[0]) * maze.node_width) // 2
        offset_y = (HEIGHT - len(matrix) * maze.node_height) // 2
        bot.set_position(start[1] * maze.node_width + offset_x,
                         start[0] * maze.node_height + offset_y)
        algorithm_complete = False

    #Tạo nút start
    img_normal = pygame.image.load("assets/sprites/play_normal.png")
    img_normal = pygame.transform.scale(img_normal, (120, 50))
    img_hover = pygame.image.load("assets/sprites/play_hover.png")
    img_hover = pygame.transform.scale(img_hover, (120, 50))
    img_pressed = pygame.image.load("assets/sprites/play_pressed.png")
    img_pressed = pygame.transform.scale(img_pressed, (120, 50))
    btn_start = Button(470, 650, 120, 50, img_normal, img_hover, img_pressed, onclick = start_algorithm)
    #Tạo nút restart
    img_normal = pygame.image.load("assets/sprites/retry_normal.png")
    img_normal = pygame.transform.scale(img_normal, (120, 50))
    img_hover = pygame.image.load("assets/sprites/retry_hover.png")
    img_hover = pygame.transform.scale(img_hover, (120, 50))
    img_pressed = pygame.image.load("assets/sprites/retry_pressed.png")
    img_pressed = pygame.transform.scale(img_pressed, (120, 50))
    btn_restart = Button(620, 650, 120, 50, img_normal, img_hover, img_pressed, onclick=restart_algorithm)
    #Algorithms selcection Card
    selection_card = AlgoCard()
    algorithms = selection_card.selected_algorithm
    algorithm_complete = False
    time_taken = None

    #Earth icon
    earth = Earth(90, 90, WIDTH, HEIGHT)

    #Nút Volume
    is_volume_on = True
    volume_on_imgs = (
        pygame.transform.scale(pygame.image.load("assets/sprites/volume_normal.png"), (40, 40)),
        pygame.transform.scale(pygame.image.load("assets/sprites/volume_hover.png"), (40, 40)),
        pygame.transform.scale(pygame.image.load("assets/sprites/volume_pressed.png"), (40, 40)),
    )
    volume_off_imgs = (
        pygame.transform.scale(pygame.image.load("assets/sprites/volume_off_normal.png"), (40, 40)),
        pygame.transform.scale(pygame.image.load("assets/sprites/volume_off_hover.png"), (40, 40)),
        pygame.transform.scale(pygame.image.load("assets/sprites/volume_off_pressed.png"), (40, 40)),
    )

    def set_volume_button_images(button, volume_on):
        normal, hover, pressed = volume_on_imgs if volume_on else volume_off_imgs
        button.img_normal = normal
        button.img_hover = hover
        button.img_pressed = pressed

    def toggle_volume():
        global is_volume_on
        is_volume_on = not is_volume_on
        set_volume_button_images(volume_btn, is_volume_on)
        #Set âm lượng của âm thanh nền
        nature_sound.set_volume(1 if is_volume_on else 0)

    volume_btn = Button(1000, 10, 40, 40, *volume_on_imgs, onclick=toggle_volume)

    while running:
        
        #Vẽ nền và mê cung
        background.draw(screen)

        #vẽ nút và giao diện
        btn_start.draw(screen)
        btn_restart.draw(screen)
        volume_btn.draw(screen)
        earth.draw(screen)
        selection_card.draw(screen)

        #Vẽ panel thống kê
        stats_panel.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            selected = selection_card.selected_algorithm
            if selected is not None:
                algorithms = selected
            btn_start.handle_event(event)
            btn_restart.handle_event(event)
            volume_btn.handle_event(event)
            selection_card.handle_event(event)
        

        maze.draw_maze(matrix, screen, WIDTH, HEIGHT, bot)
        draw_path_progression(screen, matrix, bot.path, bot.path_index, WIDTH, HEIGHT, maze.node_width)
        bot.draw(screen)
        bot.update(WIDTH, HEIGHT, matrix)
        #Update stats
        stats_panel.update_stats(
            algorithm=f"{algorithms}",
            result="Success" if algorithm_complete and len(path) > 0 else "Failure" if algorithm_complete and len(path) == 0 else "N/A",
            path_length=len(path) if path is not None and algorithm_complete else "N/A",
            execution_time=time_taken
        )
        pygame.display.flip()

    # Giống return 0 trong c++
    pygame.quit()
    
