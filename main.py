import sys

import pygame.mixer
from classes.base import *
from classes.first_level import FirstLevel

showsettings = False


class Map:
    def __init__(self):
        self.tmx_map = {0: load_pygame('tmx_files\\map_vegetable_vallue.tmx'),
                        1: load_pygame('tmx_files\\lvl2.tmx')}
        self.current_level = FirstLevel(self.tmx_map[0])

    def run(self):
        self.current_level.run()


def main():
    pygame.init()
    pygame.display.set_caption('Kirby\'s Adventure')
    image = load_image("logo.webp")
    image_cur = load_image("yellow_cursor2.png")
    pygame.display.set_icon(image)

    clock = pygame.time.Clock()
    running = True
    game_map = Map()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game_map.run()
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
        super().event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия кнопки мыши
            if self.hovered:
                self.sound.play()
                print('c')
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


    clock = pygame.time.Clock()
    running = True

    up = load_image('arrows.png')
    up = pygame.transform.scale(up, (600, 400))

    move = load_image('moving_animation.png')
    move = pygame.transform.scale(move, (200, 50))

    jump = load_image('Kirby_jump.png')
    jump = pygame.transform.scale(jump, (50, 50))

    eat = load_image('Kirby_start_eating.png')
    eat = pygame.transform.scale(eat, (80, 50))

    font = pygame.font.SysFont('comicsansms', 20)
    text_jump = font.render('1) Чтобы Кирби полетела нужно зажать стрелочку вверх',
                            True, pygame.Color('purple'))
    rect_jump = text_jump.get_rect(center=(300, 180))

    return_button = ReturnButton(10, 10, 100, 50, "MENU")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(back_ground, (0, 0))

        return_button.draw(screen)

        screen.blit(text_surface, text_rect)
        screen.blit(text_jump, rect_jump)
        screen.blit(up, (250, 200))
        screen.blit(move, (360, 300))
        screen.blit(jump, (300, 200))
        screen.blit(eat, (300, 430))
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
    pygame.init()
    menu_sound = pygame.mixer.Sound('sound\\menu_sound.mp3')
    menu_sound.play(-1)
    # print(pygame.font.get_fonts()) системные шрифты
    pygame.display.set_caption("Menu")
    back_ground = load_image("clouds.jpg")

    # изменяем размер картинки
    back_ground = pygame.transform.scale(back_ground, (700, 525))
    screen.fill((255, 255, 255))
    running = True

    play_button = PlayButton(WIDTH // 2 - 75, 250, 150, 50, "PLAY")
    exit_button = ExitButton(WIDTH // 2 - 75 , 440, 150, 50, "EXIT")
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
    sound_btn = ImageButton((370, 320),'sound_play.png', 'sound_play_hovered.png' )



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
                sound_btn.draw()
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

            if pygame.mouse.get_focused():
                x, y = pygame.mouse.get_pos()
                # изображение курсора
                screen.blit(image, (x, y))

            pygame.mouse.set_visible(False)


        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main_menu()