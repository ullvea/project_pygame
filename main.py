import sys

from classes.base import *
from classes.first_level import FirstLevel
from classes.objects import *
import pygame.mixer


class Map:
    """Класс, отвечающий за создание игры и переключение уровней"""

    def __init__(self):
        self.tmx_map = {0: load_pygame('tmx_files\\map_vegetable_vallue.tmx'),
                        1: load_pygame('tmx_files\\lvl2.tmx'),
                        2: load_pygame('tmx_files\\lvl3.tmx')}
        self.key = 0
        self.current_level = FirstLevel(self.tmx_map[1])

    def run(self, stop_game):
        self.current_level.run(stop_game)
        if pygame.sprite.spritecollideany(self.current_level.kirby, next_lvl_sprites):
            loading()
            if self.key + 1 < len(self.tmx_map):
                self.key += 1
            clear_groups()
            cur.execute(f"""UPDATE score SET last_results = {get_score()}""")
            max_result = cur.execute("""SELECT max_results FROM score""").fetchone()[0]
            if max_result < get_score():
                cur.execute(f"""UPDATE score SET max_results = {get_score()}""")
            con.commit()  # Cохраняем изменения в БД
            update_score(0)  # При переходе на новый уровень сбрасываем счётчик очков
            self.current_level = FirstLevel(self.tmx_map[self.key])


class PlayButton(Button):
    """Класс, отвечающий за создание кнопки для начала игры"""

    def __init__(self, x, y, width, height, text):
        super().__init__(x, y, width, height, text)

    def event(self, event):
        super().event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия кнопки мыши
            if self.hovered:
                main()


class SettingsButton(Button):
    """Класс, отвечающий за создание кнопки для настроек"""

    def __init__(self, x, y, width, height, text):
        super().__init__(x, y, width, height, text)

    def event(self, event):
        global showsettings
        super().event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия кнопки мыши
            if self.hovered:
                showsettings = True
                # screen.blit(self.screen_im, (100, 120))


class ExitButton(Button):
    """Класс, отвечающий за создание кнопки для выхода из игры"""

    def __init__(self, x, y, width, height, text):
        super().__init__(x, y, width, height, text)

    def event(self, event):
        super().event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия кнопки мыши
            if self.hovered:
                pygame.time.delay(300)
                pygame.quit()
                sys.exit()


class RulesButton(Button):
    """Класс, отвечающий за создание кнопки для показа правил"""

    def __init__(self, x, y, width, height, text):
        super().__init__(x, y, width, height, text)

    def event(self, event):
        super().event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия кнопки мыши
            if self.hovered:
                rule()


class ReturnButton(Button):
    def __init__(self, x, y, width, height, text):
        super().__init__(x, y, width, height, text)

    def event(self, event):
        global showsettings
        super().event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия кнопки мыши
            if self.hovered:
                showsettings = False
                main_menu()


class AgainButton(Button):
    def __init__(self, x, y, width, height, text):
        super().__init__(x, y, width, height, text)

    def event(self, event):
        global showsettings
        super().event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия кнопки мыши
            if self.hovered:
                showsettings = False



class PauseButton(ImageButton):
    def __init__(self, pos, image, hovered_image, scale):
        super().__init__(pos, image, hovered_image, scale)

    def event(self, event):
        global stop_game
        super().event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия кнопки мыши
            if self.hovered:
                stop_game = True


class PauseStopButton(ImageButton):
    def __init__(self, pos, image, hovered_image, scale):
        super().__init__(pos, image, hovered_image, scale)

    def event(self, event):
        global stop_game
        super().event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия кнопки мыши
            if self.hovered:
                stop_game = False


class SoundButton(ImageButton):
    def __init__(self, pos, image, hovered_image, scale):
        super().__init__(pos, image, hovered_image, scale)

    def event(self, event):
        super().event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия кнопки мыши
            if self.hovered:
                update_sound(True)
                pygame.mixer.stop()
                menu_sound.stop()


class SoundStopButton(ImageButton):
    def __init__(self, pos, image, hovered_image, scale):
        super().__init__(pos, image, hovered_image, scale)

    def event(self, event):
        super().event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия кнопки мыши
            if self.hovered:
                update_sound(False)
                menu_sound.play(-1)


class MapButton(ImageButton):
    def __init__(self, pos, image, hovered_image, scale):
        super().__init__(pos, image, hovered_image, scale)

    def event(self, event):
        global stop_sound
        super().event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия кнопки мыши
            if self.hovered:
                map()


def loading():
    image_cur = load_image("yellow_cursor2.png")
    running = True

    font = pygame.font.Font('font.ttf', 50)
    text_surface1 = font.render('loading', True, pygame.Color('black'))
    text_surface2 = font.render('loading.', True, pygame.Color('black'))
    text_surface3 = font.render('loading..', True, pygame.Color('black'))
    text_surface4 = font.render('loading...', True, pygame.Color('black'))
    text_rect = text_surface1.get_rect(center=(350, 100))
    text_surface = [text_surface1, text_surface1, text_surface1, text_surface1,
                    text_surface2, text_surface2, text_surface2, text_surface2,
                    text_surface3, text_surface3, text_surface3, text_surface3,
                    text_surface4, text_surface4, text_surface4, text_surface4]
    cnt = 0

    frames = []
    delay = 75
    for filename in os.listdir("loading"):
        frame = pygame.image.load(os.path.join("loading", filename))
        frames.append(frame)
    image_ind = 0
    last_delay = pygame.time.get_ticks()
    start = pygame.time.get_ticks()
    while running:
        current = pygame.time.get_ticks()
        if current - start > 3000:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        screen.blit(text_surface[cnt % 16], text_rect)
        cnt += 1

        if current - last_delay > delay:
            last_delay = current
            image_ind += 1
        screen.blit(frames[image_ind % len(frames)], (130, 150))
        if pygame.mouse.get_focused():
            x, y = pygame.mouse.get_pos()
            # изображение курсора
            screen.blit(image_cur, (x, y))
        pygame.mouse.set_visible(False)
        pygame.display.flip()
        clock.tick(FPS)


def main():
    global stop_game
    defeat_sound_play = False

    image_cur = load_image("yellow_cursor2.png")
    strip_image = pygame.image.load('data\\Objects_images\\strip.png')
    strip_image = pygame.transform.scale(strip_image, (700, 80))
    image_finish = load_image("idiot.jpg")
    image_finish = pygame.transform.scale(image_finish, (700, 525))
    fail_kirbi = load_image('sad_kirbi.png')
    fail_kirbi = pygame.transform.scale(fail_kirbi, (170, 150))

    gray_color = (128, 128, 128)
    mask_alpha = 200

    return_button = ReturnButton(100, 400, 100, 50, "MENU")
    again = AgainButton(500, 400, 100, 50, "AGAIN")
    return_button_pause = ReturnButton(100, 460, 100, 50, "MENU")
    again_pause = AgainButton(500, 460, 100, 50, "AGAIN")
    return_button_pause.color = (128, 128, 128)
    again_pause.color = (128, 128, 128)
    pause_btns = [return_button_pause, again_pause]
    defeat_btns = [return_button, again]
    pause_button = PauseButton((650, 0), 'pause_btn.png', 'pause_btn_hovered.png', scale=0.5)
    pause_stop_button = PauseStopButton((650, 0), 'pause_stop_btn.png',
                                        'pause_stop_btn_hovered.png', scale=0.5)
    sound_btn = SoundButton((320, 450), 'sound_play.png', 'sound_play_hovered.png', scale=1)
    sound_not_btn = SoundStopButton((320, 450), 'sound_not_play.png', 'sound_not_play_hovered.png',
                                    scale=1)

    game_map = Map()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not stop_game:
                pause_button.event(event)
            else:
                pause_stop_button.event(event)
        stop_game_defeat = game_map.current_level.kirby.hearts.update_game()
        game_map.run(stop_game or stop_game_defeat)
        draw_score()

        if stop_game_defeat:
            menu_sound.stop()
            if not defeat_sound_play:
                defeat_sound.play()
                defeat_sound_play = True
            screen.blit(image_finish, (0, 0))

            for i in defeat_btns:
                i.event(event)
                i.draw()

            screen.blit(fail_kirbi, (400, 100))

        elif not stop_game:
            pause_button.draw()
        else:
            mask_surf = pygame.Surface((WIDTH, HEIGHT))
            mask_surf.fill(gray_color)
            mask_surf.set_alpha(mask_alpha)
            screen.blit(mask_surf, (0, 0))
            pause_stop_button.draw()
            screen.blit(strip_image, (0, 450))
            for i in pause_btns:
                i.event(event)
                i.draw()
            if not get_state_sound():
                sound_btn.draw()
                sound_btn.event(event)
            else:
                sound_not_btn.draw()
                sound_not_btn.event(event)

        if pygame.mouse.get_focused():
            x, y = pygame.mouse.get_pos()
            # изображение курсора
            screen.blit(image_cur, (x, y))

        pygame.mouse.set_visible(False)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


def map():
    image_cur = load_image("yellow_cursor2.png")
    lvl1_map = pygame.image.load("data\\Objects_images\\map_background\\1lvl_map.png")
    lvl2_map = pygame.image.load("data\\Objects_images\\map_background\\2lvl_map.png")
    lvl3_map = pygame.image.load("data\\Objects_images\\map_background\\3lvl_map.png")
    lvl4_map = pygame.image.load("data\\Objects_images\\map_background\\4lvl_map.png")
    back_ground = pygame.transform.scale(lvl1_map, (700, 525))

    font = pygame.font.Font('1stenterprises3D.ttf', 70)
    text_surface = font.render('LEVEL MAP', True, pygame.Color('black'))
    text_rect = text_surface.get_rect(center=(350, 100))

    return_button = ReturnButton(10, 10, 100, 50, "MENU")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            screen.blit(back_ground, (0, 0))

            return_button.draw()

            screen.blit(text_surface, text_rect)

            if pygame.mouse.get_focused():
                x, y = pygame.mouse.get_pos()
                # изображение курсора
                screen.blit(image_cur, (x, y))

            return_button.event(event)
            pygame.mouse.set_visible(False)
            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()


def rule():
    image_cur = load_image("yellow_cursor2.png")

    back_ground = load_image("clouds_rules.jpg")
    back_ground = pygame.transform.scale(back_ground, (700, 525))

    font = pygame.font.Font('1stenterprises3D.ttf', 100)
    text_surface = font.render('RULES', True, pygame.Color('black'))
    text_rect = text_surface.get_rect(center=(350, 100))

    running = True

    return_button = ReturnButton(10, 10, 100, 50, "MENU")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            screen.blit(back_ground, (0, 0))

            return_button.draw()

            screen.blit(text_surface, text_rect)

            if pygame.mouse.get_focused():
                x, y = pygame.mouse.get_pos()
                # изображение курсора
                screen.blit(image_cur, (x, y))

            return_button.event(event)
            pygame.mouse.set_visible(False)
            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()


def main_menu():
    global showsettings
    menu_sound.stop()
    menu_sound.play(-1)
    # print(pygame.font.get_fonts()) системные шрифты
    back_ground = load_image("clouds.jpg")

    # изменяем размер картинки
    back_ground = pygame.transform.scale(back_ground, (700, 525))
    screen.fill((255, 255, 255))
    running = True

    play_button = PlayButton(WIDTH // 2 - 75, 250, 150, 50, "PLAY")
    exit_button = ExitButton(WIDTH // 2 - 75, 440, 150, 50, "EXIT")
    rules_button = RulesButton(WIDTH // 2 - 75, 310, 150, 50, "RULES")
    settings_button = SettingsButton(WIDTH // 2 - 75, 370, 150, 50, "SETTINGS")
    map_button = MapButton((400, 320), 'map_icon_earth.png', 'map_icon_earth_hovered.png', scale=0.25)
    menu_btns = [play_button, exit_button, rules_button, settings_button, map_button]

    max_result = str(cur.execute("""SELECT max_results FROM score""").fetchone()[0])
    last_result = str(cur.execute("""SELECT last_results FROM score""").fetchone()[0])

    font = pygame.font.Font('font.ttf', 30)
    text_surface = font.render(f"MAX SCORE: {max_result}", True, pygame.Color('black'))
    text_rect = text_surface.get_rect()
    text_rect.center = (260, 270)
    text_surface1 = font.render(f"YOUR LAST SCORE: {last_result}", True, pygame.Color('black'))
    text_rect1 = text_surface1.get_rect()
    text_rect1.center = (305, 310)
    text_surface2 = font.render("SOUND:", True, pygame.Color('black'))
    text_rect2 = text_surface2.get_rect()
    text_rect2.center = (210, 350)

    sound_btn = SoundButton((370, 320), 'sound_play.png', 'sound_play_hovered.png', scale=1)
    sound_not_btn = SoundStopButton((370, 320), 'sound_not_play.png', 'sound_not_play_hovered.png',
                                    scale=1)
    exit_settings = ReturnButton(WIDTH // 2 - 120, 420, 240, 50, "EXIT SETTINGS")

    image = load_image("yellow_cursor2.png")
    screen_im = load_image('settings_image.png', [], 2.6)

    title = load_image("kirbi.webp")
    title = pygame.transform.scale(title, (400, 200))

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # отрисовка заднего фона
            screen.blit(back_ground, (0, 0))

            # отрисовка названия
            screen.blit(title, (WIDTH // 2 - 200, 20))
            if showsettings:
                screen.blit(screen_im, (100, 220))
                if not get_state_sound():
                    sound_btn.draw()
                    sound_btn.event(event)
                else:
                    sound_not_btn.draw()
                    sound_not_btn.event(event)

                exit_settings.draw()
                exit_settings.event(event)
                screen.blit(text_surface, text_rect)
                screen.blit(text_surface1, text_rect1)
                screen.blit(text_surface2, text_rect2)

            else:
                for i in menu_btns:
                    i.draw()
                    i.event(event)

            if get_state_sound():
                menu_sound.stop()

            if pygame.mouse.get_focused():
                x, y = pygame.mouse.get_pos()
                # изображение курсора
                screen.blit(image, (x, y))

            pygame.mouse.set_visible(False)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main_menu()
