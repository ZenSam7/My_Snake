import pygame
import random
import time

try:

    snake_color = (130, 130, 150)  # Цвет змеи
    food_color = (150, 30, 33)  # Цвет еды
    text_color_GAME_OVER = (140, 190, 210)  # Цвет надписи GAME OVER
    background_color = (20, 20, 30)  # Цвет фона

    window_width = 1000  # Ширина / Высота окна
    window_height = 650
    cell_size = 50  # Размер 1 клетки
    size_text_GAME_OVER = 3  # Размер надписи GAME OVER

    speed = 0.08  # Скорость игры


    ####################################  НеКостомизируемые (обязательные) Переменные

    score = 0  # Сколько у нас очков изначально (не влияет на размер змейки)
    food_position = [0, 0]  # X/Y еды
    need_for_food = True  # Нужна ли еда
    growth = False    # Если хотим расти: True
    RUN = True  # Идёт ли игра
    variable_to_remove_one_bug = True  # Переменная, для удаления одного бага
    restart = False

    change_direction_to = ""  # Записываем куда ХОТИМ двигаться
    direction_move = "RIGHT"  # Куда мы двигаемся

    # Начальное положение змеи (сначала голова, потом хвост) (x, y) {слева в центре экрана}
    body_position = [[cell_size, 0], [0, 0]]
    # for i in range(2, 16):
    #     body_position.insert(0, [cell_size*i, 0])
    head_position = [cell_size * len(body_position), 0]  # Положение головы {слева сверху экрана}

    ####################################



    def window():
        """Создаём окно и его заголовок"""
        global wind
        wind = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("(*^ω^)    Змейка")



    def game_over():
        """Game Over"""
        global RUN, restart
        RUN = False
        size_text = size_text_GAME_OVER        # Сокращение

        font = pygame.font.Font(None, int(cell_size * size_text**0.5))    # Какой шрифт и размер надписи
        font_RESTART = pygame.font.Font(None, int(cell_size * size_text**0.5 *0.5)) # Какой шрифт и размер надписи RESTART

        text_GAME_OVER = font.render("Game Over", True, (text_color_GAME_OVER))
        text_SCORE = font.render(f"  Score = {score}", True, (text_color_GAME_OVER))
        text_RESTART = font.render("'R' = Restart", True, (text_color_GAME_OVER))

        # Выводим текст Game Over (и Score с Restart)
        wind.blit(text_GAME_OVER, (window_width // size_text, window_height // size_text))
        wind.blit(text_SCORE, (window_width // size_text, window_height // size_text + cell_size *size_text))
        wind.blit(text_RESTART, (window_width // size_text, window_height // size_text + cell_size *size_text *2))

        pygame.display.update()

        while not restart:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if event.key == ord('r'):
                        restart = True
                # Нажали крестик - выходим
                elif event.type == pygame.QUIT:
                    pygame.quit()

        RESET()



    def RESET():
        global score, food_position, need_for_food, RUN, variable_to_remove_one_bug, change_direction_to, direction_move, body_position, head_position, restart
        restart = False

        # Ресетаем все переменные
        score=0
        food_position=[0, 0]
        need_for_food=True
        RUN=True
        variable_to_remove_one_bug=True
        change_direction_to=""
        direction_move="RIGHT"
        body_position=[[cell_size, 0], [0, 0]]
        head_position=[cell_size * len(body_position), 0]
        restart = False


        pygame.display.quit()
        pygame.init()





    def draw():
        """Рисуем змейку"""
        global size_text_GAME_OVER, wind

        window()
        wind.fill((background_color))

        pygame.draw.rect(wind, food_color, (food_position[0], food_position[1], cell_size, cell_size))
        for segment in body_position:
            pygame.draw.rect(wind, snake_color, (segment[0], segment[1], cell_size, cell_size))

        # Выводим сколько у нас очков
        font = pygame.font.Font(None, int(cell_size * size_text_GAME_OVER ** 0.5 / 2))  # Какой шрифт и размер надписи
        text_SCORE = font.render(f"Score = {score}", True, (text_color_GAME_OVER))
        wind.blit(text_SCORE, (0, 0))

        pygame.display.update()




    def direction_of_move():
        def where_move():
            """Узнаём куда игрок хочет двигать змею"""
            global change_direction_to, variable_to_remove_one_bug
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and variable_to_remove_one_bug:
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        change_direction_to = "RIGHT"
                    elif event.key == pygame.K_LEFT or event.key == ord('a'):
                        change_direction_to = "LEFT"
                    elif event.key == pygame.K_UP or event.key == ord('w'):
                        change_direction_to = "UP"
                    elif event.key == pygame.K_DOWN or event.key == ord('s'):
                        change_direction_to = "DOWN"
                    # Нажали escape - выходим
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    variable_to_remove_one_bug = False
                # Нажали крестик - выходим
                elif event.type == pygame.QUIT:
                    pygame.quit()

        def possible_to_move():
            def player():
                """Если игрок хочет двигаться строго обратно,
                   То не позволяем это сделать"""
                global direction_move
                if any((
                        change_direction_to == "RIGHT" and not direction_move == "LEFT",
                        change_direction_to == "LEFT" and not direction_move == "RIGHT",
                        change_direction_to == "UP" and not direction_move == "DOWN",
                        change_direction_to == "DOWN" and not direction_move == "UP"
                )):
                    direction_move=change_direction_to

            def screen_borders():
                global head_position, body_position
                """Если голова выходит за экран,
                   Или голова врезается в тело - game over"""
                if any((
                        # Проверяем выходит ли голова за экран
                        head_position[0] == 0 - cell_size,
                        head_position[0] == window_width,
                        head_position[1] == 0 - cell_size,
                        head_position[1] == window_height
                    )):
                    game_over()

                    # Проверяем врезается ли голова в тело
                for segment in body_position:
                    if head_position == segment:
                        game_over()

            player()
            screen_borders()

        where_move()
        possible_to_move()



    def move_snake():
        """Двигаем змею"""
        global variable_to_remove_one_bug
        if direction_move == "RIGHT":
            if not need_for_food:
                body_position.pop()      # Удаляем конец хвоста, если мы не удлиняемся
            body_position.insert (0, [head_position[0], head_position[1]]) # Добавляем начало к хвосту
            head_position[0] += cell_size         # Двигаем голову вправо
        elif direction_move == "LEFT":
            if not need_for_food:
                body_position.pop()
            body_position.insert (0, [head_position[0], head_position[1]])
            head_position[0] -= cell_size  # Двигаем голову влево
        elif direction_move == "UP":
            if not need_for_food:
                body_position.pop()
            body_position.insert (0, [head_position[0], head_position[1]])
            head_position[1] -= cell_size  # Двигаем голову вверх
        elif direction_move == "DOWN":
            if not need_for_food:
                body_position.pop()
            body_position.insert (0, [head_position[0], head_position[1]])
            head_position[1] += cell_size  # Двигаем голову вниз
        variable_to_remove_one_bug = True



    def spawn_food():
        """Создаём координаты еды"""
        global need_for_food, food_position
        if need_for_food:
            food_position = [random.randint(1, window_width // cell_size - 2),
                                  random.randint(1, window_height // cell_size - 2)]

            food_position[0] *= cell_size
            food_position[1] *= cell_size

            # Если еда заспавнилась в змее
            for segment in body_position:
                if food_position == segment:
                    spawn_food()

            need_for_food = False



    def food_eaten():
        """Съедена ли еда"""
        global food_position, need_for_food, score
        # Если X/Y еды совпадает с X/Y головы, то съедаем
        if food_position == head_position:
            food_position = [0, 0]
            need_for_food = True
            score += 1



    #################################################################################################

    while True:
        pygame.init()
        pygame.display.quit()
        # Game
        window()
        while RUN:
            food_eaten()
            move_snake()
            spawn_food()
            draw()
            for i in range(60):     # Что бы управление ощущалось лучше
                direction_of_move()
                time.sleep(speed/60)


except:
    pass  # ¯＼_(._.)_/¯