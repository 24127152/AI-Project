import pygame 
from Maze import Maze
from Background import Background
from Bot import Bot
from IDA import ida_star
from Algorithms import A_search, UCS, Beam_search
from Button import Button
from AlgoCard import AlgoCard
from StatsPanel import StatsPanel
from Earth import Earth
from Flag import Flag
from LegendPanel import draw_legend_panel, Star
from Slider import Slider
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


def draw_search_progression(screen, matrix, explored_nodes, progress_index, width, height, tile_size):
    if not explored_nodes:
        return

    W = len(matrix[0]) * tile_size
    H = len(matrix) * tile_size
    offset_x = (width - W) // 2
    offset_y = (height - H) // 2

    last = min(progress_index, len(explored_nodes) - 1)
    for k in range(last + 1):
        i, j = explored_nodes[k]
        x = offset_x + j * tile_size + tile_size // 2 - 4
        y = offset_y + i * tile_size + tile_size // 2 - 4
        pygame.draw.rect(screen, (64, 196, 255), (x, y, 8, 8))

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
    pending_path = []
    exploration_order = []
    exploration_progress = 0
    explore_nodes_per_frame = 2
    
    #Tạo bot
    bot = Bot("assets/sprites/bot.png", path, maze.node_width, maze.node_height)
    start, goal = maze.find_pos(matrix, (0, 0), (len(matrix) - 1, len(matrix[0]) - 1), bot, WIDTH, HEIGHT)
    running = True
    algorithm_running = False
    
    #Điều chính kích thước ma trận
    def resize_maze(new_size):
        global matrix, start, goal, algorithm_running, path, pending_path, exploration_order, exploration_progress
        algorithm_running = False
        path = []
        pending_path = []
        exploration_order = []
        exploration_progress = 0
        
        # Tạo maze mới
        matrix = maze.generate_maze(new_size)
        
        # Tìm start và goal mới
        start, goal = maze.find_pos(matrix, (0, 0), (len(matrix) - 1, len(matrix[0]) - 1), bot, WIDTH, HEIGHT)
        
        # Reset bot
        bot.path = []
        bot.path_index = 0
        bot.is_moving = False
        
        # Đặt bot ở vị trí start
        offset_x = (WIDTH - len(matrix[0]) * maze.node_width) // 2
        offset_y = (HEIGHT - len(matrix) * maze.node_height) // 2
        bot.set_position(start[1] * maze.node_width + offset_x,
                         start[0] * maze.node_height + offset_y)
    
    def start_algorithm(bot):
        global algorithm_running, path, pending_path, exploration_order, exploration_progress, time_taken, algorithm_complete
         
        if not algorithm_running:
            start_perf = time.perf_counter()
            #Lựa chọn thuật toán
            if algorithms == "A Star":
                result = A_search(matrix, start, goal)
                path = result["path_found"] or []
                exploration_order = result.get("exploration_order", [])
                time_taken = result["processing_time_ms"] / 1000
            elif algorithms == "IDA Star":
                result = ida_star(matrix, start, goal, return_details=True)
                path = result["path_found"] or []
                exploration_order = result.get("exploration_order", [])
                time_taken = result["processing_time_ms"] / 1000
            elif algorithms == "UCS":
                result = UCS(matrix, start, goal)
                path = result["path_found"] or []
                exploration_order = result.get("exploration_order", [])
                time_taken = result["processing_time_ms"] / 1000
            elif algorithms == "Beam Search":
                result = Beam_search(matrix, start, goal)
                path = result["path_found"] or []
                exploration_order = result.get("exploration_order", [])
                time_taken = result["processing_time_ms"] / 1000
            else:
                path = []
                exploration_order = []
                end_time = time.perf_counter()
                time_taken = end_time - start_perf

            pending_path = path[:]
            exploration_progress = 0
            bot.path = []
            bot.path_index = 0
            algorithm_running = True
            algorithm_complete = False
            bot.is_moving = True

        if not exploration_order:
            algorithm_complete = True
        
            
    #Reset thuật toán
    def restart_algorithm(bot):
        global algorithm_running, path, pending_path, exploration_order, exploration_progress, time_taken, algorithm_complete
        path = []
        pending_path = []
        exploration_order = []
        exploration_progress = 0
        bot.path = path
        bot.is_moving = False
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
    btn_start = Button(470, 650, 120, 50, img_normal, img_hover, img_pressed, onclick=lambda: start_algorithm(bot))
    #Tạo nút restart
    img_normal = pygame.image.load("assets/sprites/retry_normal.png")
    img_normal = pygame.transform.scale(img_normal, (120, 50))
    img_hover = pygame.image.load("assets/sprites/retry_hover.png")
    img_hover = pygame.transform.scale(img_hover, (120, 50))
    img_pressed = pygame.image.load("assets/sprites/retry_pressed.png")
    img_pressed = pygame.transform.scale(img_pressed, (120, 50))
    btn_restart = Button(620, 650, 120, 50, img_normal, img_hover, img_pressed, onclick=lambda: restart_algorithm(bot))
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

    #Hàm tắt, mở âm thanh
    def toggle_volume():
        global is_volume_on
        is_volume_on = not is_volume_on
        set_volume_button_images(volume_btn, is_volume_on)
        #Set âm lượng của âm thanh nền
        nature_sound.set_volume(1 if is_volume_on else 0)

    volume_btn = Button(1000, 10, 40, 40, *volume_on_imgs, onclick=toggle_volume)

    #Tạo thanh trượt chỉnh kích thước grid
    slider = Slider(500, 150, 200, 5, min_value=9, max_value=15, initial_value=9, on_apply=resize_maze)
    #Vẽ lá cờ Goal
    goal_flag = Flag(50, 50)
    start_flag = Star(50, 50)
    
    while running:
        
        #Vẽ nền và mê cung
        background.draw(screen)

        #vẽ nút và giao diện
        btn_start.draw(screen)
        btn_restart.draw(screen)
        volume_btn.draw(screen)
        earth.draw(screen)
        selection_card.draw(screen)
        #Vẽ panel chú thích
        draw_legend_panel(screen, 500, 700)

        slider.draw(screen)

        #Vẽ panel thống kê
        stats_panel.draw(screen)
        
        #Vẽ cờ bắt đầu
        start_offset_x = (WIDTH - len(matrix[0]) * maze.node_width) // 2
        start_offset_y = (HEIGHT - len(matrix) * maze.node_height) // 2
        start_tile_x = start_offset_x + start[1] * maze.node_width
        start_tile_y = start_offset_y + start[0] * maze.node_height
        start_flag.draw(screen, start_tile_x + maze.node_width // 2,
                             start_tile_y + maze.node_height // 2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            btn_start.handle_event(event)
            btn_restart.handle_event(event)
            volume_btn.handle_event(event)
            slider.handle_event(event)
            selected = selection_card.handle_event(event)

            if selected is not None:
                algorithms = selected
        
        #Vẽ ma trận và đường đi
        maze.draw_maze(matrix, screen, WIDTH, HEIGHT, bot)

        #Vẽ tiến trình đi
        if algorithm_running and exploration_progress < len(exploration_order):
            exploration_progress = min(exploration_progress + explore_nodes_per_frame, len(exploration_order))

        draw_search_progression(screen, matrix, exploration_order, exploration_progress, WIDTH, HEIGHT, maze.node_width)

        if algorithm_running and exploration_progress >= len(exploration_order):
            if not bot.path and pending_path:
                bot.path = pending_path
                bot.path_index = 0

        if algorithm_running and bot.path:
            bot.update(WIDTH, HEIGHT, matrix)
            if bot.path_index >= len(bot.path):
                algorithm_running = False
                algorithm_complete = True
        elif algorithm_running and not pending_path and exploration_progress >= len(exploration_order):
            algorithm_running = False
            algorithm_complete = True

        draw_path_progression(screen, matrix, bot.path, bot.path_index, WIDTH, HEIGHT, maze.node_width)
        bot.draw(screen)

        #Vẽ cờ goal
        goal_offset_x = (WIDTH - len(matrix[0]) * maze.node_width) // 2
        goal_offset_y = (HEIGHT - len(matrix) * maze.node_height) // 2
        goal_tile_x = goal_offset_x + goal[1] * maze.node_width
        goal_tile_y = goal_offset_y + goal[0] * maze.node_height
        goal_flag.draw(screen, goal_tile_x + maze.node_width // 2,
                                goal_tile_y + maze.node_height // 2 - goal_flag.height // 2)
        
        #Cập nhật thông số
        stats_panel.update_stats(
            algorithm=f"{algorithms}",
            result="Success" if algorithm_complete and len(path) > 0 else "Failure" if algorithm_complete and len(path) == 0 else "N/A",
            path_length=len(path) if path is not None and algorithm_complete else "N/A",
            execution_time=time_taken
        )
        pygame.display.flip()

    # Giống return 0 trong c++
    pygame.quit()
    
