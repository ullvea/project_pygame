from classes.base import *


pygame.display.set_caption("Menu")
back_ground = load_image("menu_white_and_purple.jpg")
back_ground = pygame.transform.scale(back_ground, (700, 525))
screen.fill((255, 255, 255))


def main_menu():
    while True:
        screen.blit(back_ground, (0, 0))

        pygame.display.flip()


main_menu()