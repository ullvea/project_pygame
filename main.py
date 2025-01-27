import sys

import pygame.mixer

from classes.base import *
from classes.first_level import FirstLevel


class Map:
    def __init__(self):
        self.tmx_map = {0: load_pygame('tmx_files\\map_vegetable_vallue.tmx'),
                        1: load_pygame('tmx_files\\map_vegetable_vallue_2.tmx')}
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


def main_menu():
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

    play_button = PlayButton(290, 290, 100, 50, "PLAY")
    exit_button = ExitButton(290, 440, 100, 50, "EXIT")

    image = load_image("yellow_cursor2.png")

    title = load_image("kirbi.webp")
    title = pygame.transform.scale(title, (300, 200))

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # отрисовка заднего фона
            screen.blit(back_ground, (0, 0))
            # отрисовка кнопки
            play_button.draw(screen)
            # screen.blit(button_image1, button_rect1)

            play_button.draw(screen)
            exit_button.draw(screen)
            # отрисовка названия
            screen.blit(title, (200, 50))

            if pygame.mouse.get_focused():
                x, y = pygame.mouse.get_pos()
                # изображение курсора
                screen.blit(image, (x, y))

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if button_rect1.collidepoint(event.pos):
            #         print("Кнопка нажата!")

            pygame.mouse.set_visible(False)

            play_button.event(event)
            exit_button.event(event)

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main_menu()
