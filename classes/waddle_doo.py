from classes.base import *
from classes.kirby import Kirby

class WaddleDoo(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        colorkeys = [(98, 130, 179), (116, 154, 212), (111, 147, 201), (84, 110, 140)]
        self.image = load_image('waddle_doo.png', colorkeys)
        self.animation =  AnimatedSprite(load_image('waddle_doo.png', colorkeys),
                                         2, 1, 36, 16)
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        self.image = self.animation.image
        self.animation.update()
