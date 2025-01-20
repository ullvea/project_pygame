from classes.base import *


pygame.display.set_caption("Menu")
back_ground = pygame.image.load("data/menu_white_and_purple.jpg")
screen.fill((255, 255, 255))


def main_menu():
    while True:
        screen.blit(back_ground, (0, 0))

        pygame.display.flip()


main_menu()