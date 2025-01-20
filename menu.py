from classes.base import *


pygame.display.set_caption("Menu")
BG = pygame.image.load("Background.png")


def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        pygame.display.flip()


main_menu()