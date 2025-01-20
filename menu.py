from classes.base import *


def main_menu():
    pygame.init()
    pygame.display.set_caption("Menu")
    back_ground = load_image("menu_white_and_purple.jpg")
    back_ground = pygame.transform.scale(back_ground, (700, 525))
    screen.fill((255, 255, 255))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(back_ground, (0, 0))

        pygame.display.flip()
    pygame.quit()


main_menu()
