import sys

from classes.base import *
from classes.first_level import FirstLevel
from classes.objects import *
import pygame.mixer

showsettings = False


class Map:
    def __init__(self):
        self.tmx_map = {0: load_pygame('tmx_files\\map_vegetable_vallue.tmx'),
                        1: load_pygame('tmx_files\\lvl2.tmx')}
        self.key = 0
        self.current_level = FirstLevel(self.tmx_map[self.key])

    def run(self, stop_game):
        self.current_level.run(stop_game)
        if pygame.sprite.spritecollideany(self.current_level.kirby, next_lvl_sprites):
            loading()
            self.key += 1
            clear_groups()
            self.current_level = FirstLevel(self.tmx_map[self.key])


def loading():
    pygame.init()
    pygame.display.set_caption('Kirby\'s Adventure')
    image = load_image("logo.webp")
    image_cur = load_image("yellow_cursor2.png")
    pygame.display.set_icon(image)
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
    # os.listdir() в Python — это метод для получения списка всех файлов и каталогов в указанном каталоге
    # Функция os.path.join() используется для объединения нескольких путей.
    # Она учитывает особенности операционной системы и добавляет соответствующий разделитель между путями

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


class PauseButton(ImageButton):
    def __init__(self, pos, image, hovered_image, scale):
        super().__init__(pos, image, hovered_image, scale)

    def event(self, event):
        global stop_game
        super().event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия кнопки мыши
            if self.hovered:
                self.sound.play()
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
                self.sound.play()
                stop_game = False


def main():
    global stop_game
    pygame.init()
    pygame.display.set_caption('Kirby\'s Adventure')
    image = load_image("logo.webp")
    image_cur = load_image("yellow_cursor2.png")
    pygame.display.set_icon(image)

    pause_button = PauseButton((650, 0), 'pause_btn.png', 'pause_btn_hovered.png', scale=0.5)
    pause_stop_button = PauseStopButton((650, 0), 'pause_stop_btn.png',
                                        'pause_stop_btn_hovered.png', scale=0.5)

    running = True
    game_map = Map()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not stop_game:
                pause_button.event(event)
            else:
                pause_stop_button.event(event)
        stop_game_defeat = game_map.current_level.kirby.hearts.update_game()
        stop_game = stop_game_defeat if stop_game_defeat else stop_game
        game_map.run(stop_game)
        if not stop_game:
            pause_button.draw()
        else:
            pause_stop_button.draw()

        if pygame.mouse.get_focused():
            x, y = pygame.mouse.get_pos()
            # изображение курсора
            screen.blit(image_cur, (x, y))

        pygame.mouse.set_visible(False)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


class PlayButton(Button):
    def __init__(self, x, y, width, height, text):
        super().__init__(x, y, width, height, text)

    def event(self, event):
        super().event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия кнопки мыши
            if self.hovered:
                self.sound.play()
                main()


class SettingsButton(Button):
    def __init__(self, x, y, width, height, text):
        super().__init__(x, y, width, height, text)

    def event(self, event):
        global showsettings
        super().event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия кнопки мыши
            if self.hovered:
                self.sound.play()
                showsettings = True
                # screen.blit(self.screen_im, (100, 120))


class ExitButton(Button):
    def __init__(self, x, y, width, height, text):
        super().__init__(x, y, width, height, text)

    def event(self, event):
        super().event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия кнопки мыши
            if self.hovered:
                self.sound.play()
                pygame.time.delay(300)
                pygame.quit()
                sys.exit()


class RulesButton(Button):
    def __init__(self, x, y, width, height, text):
        super().__init__(x, y, width, height, text)

    def event(self, event):
        super().event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия кнопки мыши
            if self.hovered:
                self.sound.play()
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
                self.sound.play()
                showsettings = False
                main_menu()


def rule():
    pygame.init()
    pygame.display.set_caption('Kirby\'s Adventure')
    image = load_image("logo.webp")
    image_cur = load_image("yellow_cursor2.png")
    pygame.display.set_icon(image)

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

            return_button.draw(screen)

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



class SoundButton(ImageButton):
    def __init__(self, pos, image, hovered_image, scale):
        super().__init__(pos, image, hovered_image, scale)

    def event(self, event):
        global stop_sound
        super().event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия кнопки мыши
            if self.hovered:
                self.sound.play()
                stop_sound = True
                menu_sound.stop()


class SoundStopButton(ImageButton):
    def __init__(self, pos, image, hovered_image, scale):
        super().__init__(pos, image, hovered_image, scale)

    def event(self, event):
        global stop_sound
        super().event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия кнопки мыши
            if self.hovered:
                self.sound.play()
                stop_sound = False
                menu_sound.play(-1)




def main_menu():
    global showsettings
    pygame.init()
    menu_sound.stop()
    menu_sound.play(-1)
    # print(pygame.font.get_fonts()) системные шрифты
    pygame.display.set_caption("Menu")
    back_ground = load_image("clouds.jpg")

    # изменяем размер картинки
    back_ground = pygame.transform.scale(back_ground, (700, 525))
    screen.fill((255, 255, 255))
    running = True

    play_button = PlayButton(WIDTH // 2 - 75, 250, 150, 50, "PLAY")
    exit_button = ExitButton(WIDTH // 2 - 75, 440, 150, 50, "EXIT")
    rules_button = RulesButton(WIDTH // 2 - 75, 310, 150, 50, "RULES")

    settings_button = SettingsButton(WIDTH // 2 - 75, 370, 150, 50, "SETTINGS")
    font = pygame.font.Font('font.ttf', 30)
    text_surface = font.render("MAX SCORE:", True, pygame.Color('black'))
    text_rect = text_surface.get_rect()
    text_rect.center = (240, 270)
    text_surface1 = font.render("YOUR MAX LEVEL:", True, pygame.Color('black'))
    text_rect1 = text_surface1.get_rect()
    text_rect1.center = (275, 310)
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
                if not stop_sound:
                    sound_btn.draw()
                    sound_btn.event(event)
                else:
                    sound_not_btn.draw()
                    sound_not_btn.event(event)
                exit_settings.draw(screen)
                exit_settings.event(event)
                screen.blit(text_surface, text_rect)
                screen.blit(text_surface1, text_rect1)
                screen.blit(text_surface2, text_rect2)

            else:
                play_button.draw(screen)
                exit_button.draw(screen)
                rules_button.draw(screen)
                rules_button.event(event)
                settings_button.draw(screen)
                play_button.event(event)
                exit_button.event(event)
                settings_button.event(event)

            if stop_sound:
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