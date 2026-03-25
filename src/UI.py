import pygame 
import random
from Maze import Maze
from Background import Background
from Bot import Bot
from Monster import Monster
from Plant import Plant
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
from project import DFS, Bidirectional_bfs

#sửa: Import Menu và hàm load ảnh
from Menu import MainMenu, load_img_safe
#sửa xong

MONSTER_COST_VALUE = 5
PLANT_COST_VALUE = 6


def get_cell_cost(cell_value):
    if cell_value == MONSTER_COST_VALUE:
        return MONSTER_COST_VALUE
    if cell_value == PLANT_COST_VALUE:
        return PLANT_COST_VALUE
    return 1


def calculate_path_cost(matrix, path):
    if not path:
        return None

    total_cost = 0
    for row, col in path[1:]:
        total_cost += get_cell_cost(matrix[row][col])
    return total_cost

#Hàm vẽ dường đi
def draw_path_progression(screen, matrix, path, progress_index, width, height, tile_size):
    if not path or progress_index < 0:
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


def spawn_monster_in_maze(matrix, start, goal, width, height, tile_size):
    candidates = []
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value == 0 and (i, j) != start and (i, j) != goal:
                candidates.append((i, j))

    if not candidates:
        return None, None

    monster_row, monster_col = random.choice(candidates)
    matrix[monster_row][monster_col] = MONSTER_COST_VALUE

    maze_width_px = len(matrix[0]) * tile_size
    maze_height_px = len(matrix) * tile_size
    offset_x = (width - maze_width_px) // 2
    offset_y = (height - maze_height_px) // 2

    monster_x = offset_x + monster_col * tile_size
    monster_y = offset_y + monster_row * tile_size
    monster = Monster(monster_x, monster_y, tile_size, tile_size)
    return monster, (monster_row, monster_col)


def spawn_plant_in_maze(matrix, start, goal, width, height, tile_size):
    candidates = []
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value == 0 and (i, j) != start and (i, j) != goal:
                candidates.append((i, j))

    if not candidates:
        return None, None

    plant_row, plant_col = random.choice(candidates)
    matrix[plant_row][plant_col] = PLANT_COST_VALUE

    maze_width_px = len(matrix[0]) * tile_size
    maze_height_px = len(matrix) * tile_size
    offset_x = (width - maze_width_px) // 2
    offset_y = (height - maze_height_px) // 2

    plant_x = offset_x + plant_col * tile_size
    plant_y = offset_y + plant_row * tile_size
    plant = Plant(plant_x, plant_y, tile_size, tile_size)
    return plant, (plant_row, plant_col)

if __name__ == "__main__":

    WIDTH = 1200
    HEIGHT = 800
    pygame.init()
    #Âm thanh nền
    nature_sound = pygame.mixer.Sound("assets/sounds/nature_sound.wav")
    nature_sound.play(-1)  # Phát âm thanh lặp lại

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    #sửa: Khởi tạo biến trạng thái và các callback cho Menu
    game_state = "MENU"

    def go_to_playing():
        global game_state; game_state = "PLAYING"
        
    def quit_game():
        global running; running = False

    main_menu = MainMenu(WIDTH, HEIGHT, go_to_playing, quit_game)
    #sửa xong

    maze = Maze(500, 500, "assets/sprites/maze.png")
    matrix  = maze.load_matrix("src/Matrix.txt")

    background = Background(WIDTH, HEIGHT, "assets/sprites/Background.png")

    stats_panel = StatsPanel()
    path = []
    total_path_cost = None
    pending_path = []
    exploration_order = []
    exploration_progress = 0
    explore_nodes_per_frame = 1
    
    #Tạo bot
    bot = Bot("assets/sprites/bot.png", path, maze.node_width, maze.node_height)
    start, goal = maze.find_pos(matrix, (0, 0), (len(matrix) - 1, len(matrix[0]) - 1), bot, WIDTH, HEIGHT)
    monsters = []
    plants = []
    spawn_count = random.randrange(1, max(2, len(matrix) // 2))
    for _ in range(spawn_count):
        monster, monster_pos = spawn_monster_in_maze(matrix, start, goal, WIDTH, HEIGHT, maze.node_width)
        plant, plant_pos = spawn_plant_in_maze(matrix, start, goal, WIDTH, HEIGHT, maze.node_width)
        if monster is not None:
            monsters.append(monster)
        if plant is not None:
            plants.append(plant)
    running = True
    algorithm_running = False
    animation_phase = None

    def move_bot_to_start():
        offset_x = (WIDTH - len(matrix[0]) * maze.node_width) // 2
        offset_y = (HEIGHT - len(matrix) * maze.node_height) // 2
        bot.set_position(start[1] * maze.node_width + offset_x,
                         start[0] * maze.node_height + offset_y)
    
    #Điều chính kích thước ma trận
    def resize_maze(new_size):
        global matrix, start, goal, algorithm_running, path, total_path_cost, pending_path, exploration_order, exploration_progress, animation_phase, monsters, plants
        algorithm_running = False
        path = []
        total_path_cost = None
        pending_path = []
        exploration_order = []
        exploration_progress = 0
        animation_phase = None
        
        # Tạo maze mới
        matrix = maze.generate_maze(new_size)
        
        # Tìm start và goal mới
        start, goal = maze.find_pos(matrix, (0, 0), (len(matrix) - 1, len(matrix[0]) - 1), bot, WIDTH, HEIGHT)

        #Spawn theo kích thước ma trận mới, spawn nhiều hơn khi kích thước lớn hơn
        monsters = []
        plants = []
        spawn_count = random.randrange(1, max(2, len(matrix) // 2))
        for _ in range(spawn_count):
            monster, monster_pos = spawn_monster_in_maze(matrix, start, goal, WIDTH, HEIGHT, maze.node_width)
            plant, plant_pos = spawn_plant_in_maze(matrix, start, goal, WIDTH, HEIGHT, maze.node_width)
            if monster is not None:
                monsters.append(monster)
            if plant is not None:
                plants.append(plant)
        
        # Reset bot
        bot.path = []
        bot.path_index = 0
        bot.is_moving = False
        
        # Đặt bot ở vị trí start
        move_bot_to_start()
    
    def start_algorithm(bot):
        global algorithm_running, path, total_path_cost, pending_path, exploration_order, exploration_progress, time_taken, algorithm_complete, animation_phase
         
        if not algorithm_running:
           
            #Lựa chọn thuật toán
            if algorithms == "A Star":
                result = A_search(matrix, start, goal)
                path = result["path_found"] or []
                total_path_cost = result.get("total_path_cost")
                exploration_order = result.get("exploration_order", [])
                time_taken = result["processing_time_ms"] / 1000
            elif algorithms == "IDA Star":
                result = ida_star(matrix, start, goal, return_details=True)
                path = result["path_found"] or []
                total_path_cost = calculate_path_cost(matrix, path)
                exploration_order = result.get("exploration_order", [])
                time_taken = result["processing_time_ms"] / 1000
            elif algorithms == "UCS":
                result = UCS(matrix, start, goal)
                path = result["path_found"] or []
                total_path_cost = result.get("total_path_cost")
                exploration_order = result.get("exploration_order", [])
                time_taken = result["processing_time_ms"] / 1000
            elif algorithms == "Beam Search":
                result = Beam_search(matrix, start, goal)
                path = result["path_found"] or []
                total_path_cost = result.get("total_path_cost")
                exploration_order = result.get("exploration_order", [])
                time_taken = result["processing_time_ms"] / 1000

            elif algorithms == "DFS":
                result = DFS(matrix, start, goal)
                path = result["path_found"] or []
                total_path_cost = result.get("total_path_cost")
                exploration_order = result.get("exploration_order", [])
                time_taken = result["processing_time_us"] / 1000000

            elif algorithms == "BDS":
                result = Bidirectional_bfs(matrix, start, goal)
                path = result["path_found"] or []
                total_path_cost = result.get("total_path_cost")
                exploration_order = result.get("exploration_order", [])
                time_taken = result["processing_time_us"] / 1000000
            else:
                path = []
                total_path_cost = None
                exploration_order = []
                end_time = time.perf_counter()
                time_taken = end_time - start_perf

            pending_path = path[:]
            exploration_progress = 0
            move_bot_to_start()
            bot.path = []
            bot.path_index = 0

            # Chạy 2 phase: vẽ explored nodes trước, sau đó bot mới đi final path.
            if exploration_order:
                animation_phase = "exploring"
                algorithm_running = True
                algorithm_complete = False
                bot.is_moving = False
            elif pending_path:
                bot.path = pending_path
                animation_phase = "final"
                algorithm_running = True
                algorithm_complete = False
                bot.is_moving = True
            else:
                bot.path = []
                animation_phase = None
                algorithm_running = False
                algorithm_complete = True
                bot.is_moving = False
        
            
    #Reset thuật toán
    def restart_algorithm(bot):
        global algorithm_running, path, total_path_cost, pending_path, exploration_order, exploration_progress, time_taken, algorithm_complete, animation_phase
        path = []
        total_path_cost = None
        pending_path = []
        exploration_order = []
        exploration_progress = 0
        animation_phase = None
        bot.path = path
        bot.is_moving = False
        bot.path_index = 0
        algorithm_running = False
        time_taken = None
        move_bot_to_start()
        algorithm_complete = False

    #sửa: Chỉnh tọa độ 3 nút điều khiển (Play - Back - Retry) nằm cân đối ở giữa màn hình
    #Nút Start (X=400)
    img_normal = pygame.image.load("assets/sprites/play_normal.png")
    img_normal = pygame.transform.scale(img_normal, (120, 50))
    img_hover = pygame.image.load("assets/sprites/play_hover.png")
    img_hover = pygame.transform.scale(img_hover, (120, 50))
    img_pressed = pygame.image.load("assets/sprites/play_pressed.png")
    img_pressed = pygame.transform.scale(img_pressed, (120, 50))
    btn_start = Button(400, 650, 120, 50, img_normal, img_hover, img_pressed, onclick=lambda: start_algorithm(bot))
    
    #Nút Back (X=550) - Hàm quay về Menu
    def back_to_menu():
        global game_state
        game_state = "MENU"
        restart_algorithm(bot)
        
    img_back_normal = load_img_safe("assets/sprites/back_normal.png", (120, 50))
    img_back_hover = load_img_safe("assets/sprites/back_hover.png", (120, 50))
    img_back_pressed = load_img_safe("assets/sprites/back_pressed.png", (120, 50))
    btn_back_game = Button(550, 650, 120, 50, img_back_normal, img_back_hover, img_back_pressed, onclick=back_to_menu)

    #Nút Restart (X=700)
    img_normal = pygame.image.load("assets/sprites/retry_normal.png")
    img_normal = pygame.transform.scale(img_normal, (120, 50))
    img_hover = pygame.image.load("assets/sprites/retry_hover.png")
    img_hover = pygame.transform.scale(img_hover, (120, 50))
    img_pressed = pygame.image.load("assets/sprites/retry_pressed.png")
    img_pressed = pygame.transform.scale(img_pressed, (120, 50))
    btn_restart = Button(700, 650, 120, 50, img_normal, img_hover, img_pressed, onclick=lambda: restart_algorithm(bot))
    #sửa xong

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
        
        #Vẽ nền chung
        background.draw(screen)

        #sửa: Tách phân luồng render (vẽ hình) cho MENU và PLAYING
        if game_state == "MENU":
            main_menu.draw(screen)

        elif game_state == "PLAYING":
            # Toàn bộ code vẽ game
            btn_start.draw(screen)
            btn_back_game.draw(screen) # Vẽ nút back
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

            #Vẽ ma trận và đường đi
            maze.draw_maze(matrix, screen, WIDTH, HEIGHT, bot)

            # Vẽ explored path từ từ theo frame, bot chưa di chuyển trong phase này.
            if animation_phase == "exploring":
                exploration_progress = min(exploration_progress + explore_nodes_per_frame, len(exploration_order))
            elif exploration_order:
                exploration_progress = len(exploration_order)

            draw_search_progression(screen, matrix, exploration_order, exploration_progress, WIDTH, HEIGHT, maze.node_width)

            if algorithm_running and animation_phase == "exploring" and exploration_progress >= len(exploration_order):
                if pending_path:
                    move_bot_to_start()
                    bot.path = pending_path
                    bot.path_index = 0
                    bot.is_moving = True
                    animation_phase = "final"
                else:
                    algorithm_running = False
                    algorithm_complete = True
                    animation_phase = None

            if algorithm_running and animation_phase == "final" and bot.path:
                bot.update(WIDTH, HEIGHT, matrix)
                if bot.path_index >= len(bot.path):
                    algorithm_running = False
                    algorithm_complete = True
                    animation_phase = None
            elif algorithm_running and animation_phase == "final" and not bot.path:
                algorithm_running = False
                algorithm_complete = True
                animation_phase = None

            final_progress = -1
            if animation_phase == "final":
                final_progress = bot.path_index
            elif algorithm_complete and pending_path:
                final_progress = len(pending_path) - 1

            draw_path_progression(screen, matrix, pending_path, final_progress, WIDTH, HEIGHT, maze.node_width)

            #Vẽ cờ bắt đầu (đè lên nếu cần)
            start_offset_x = (WIDTH - len(matrix[0]) * maze.node_width) // 2
            start_offset_y = (HEIGHT - len(matrix) * maze.node_height) // 2
            start_tile_x = start_offset_x + start[1] * maze.node_width
            start_tile_y = start_offset_y + start[0] * maze.node_height
            start_flag.draw(screen, start_tile_x + maze.node_width // 2,
                                 start_tile_y + maze.node_height // 2)

            #Vẽ bot
            bot.draw(screen)
            for monster in monsters:
                monster.draw(screen)
            for plant in plants:
                plant.draw(screen)

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
                execution_time=time_taken,
                path_cost=total_path_cost if algorithm_complete else "N/A"
            )
        #sửa xong

        #sửa: Phân luồng xử lý sự kiện Event tách biệt cho MENU và PLAYING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_state == "MENU":
                main_menu.handle_event(event) # Chỉ nhận click chuột ở Menu
                
            elif game_state == "PLAYING":
                # ESC quay lại menu
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_state = "MENU"
                    restart_algorithm(bot)
                    
                btn_start.handle_event(event)
                btn_back_game.handle_event(event) # Xử lý click nút Back
                btn_restart.handle_event(event)
                volume_btn.handle_event(event)
                slider.handle_event(event)
                selected = selection_card.handle_event(event)

                if selected is not None:
                    algorithms = selected
        #sửa xong
        
        pygame.display.flip()

    # Giống return 0 trong c++
    pygame.quit()