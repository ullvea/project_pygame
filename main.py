from classes.base import *
from classes.first_level import FirstLevel


class Map:
    def __init__(self):
        self.tmx_map = {0: load_pygame('tmx_files\\map_vegetable_vallue.tmx')}
        self.current_level = FirstLevel(self.tmx_map[0])

    def run(self):
        self.current_level.run()


def main():
    pygame.init()
    pygame.display.set_caption('Kirby\'s Adventure')
    image = load_image("logo.webp")
    pygame.display.set_icon(image)

    clock = pygame.time.Clock()
    running = True
    game_map = Map()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game_map.run()

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()
