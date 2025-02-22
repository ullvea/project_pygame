from classes.base import *

class Hearts(pygame.sprite.Sprite):
    ''' Класс отвечает за жизни игрока '''

    def __init__(self):
        super().__init__(objects_sprites)
        self.colorkeys = []
        self.animation = AnimatedSprite(load_image('hearts.png', self.colorkeys),
                                        1, 5, 1000, 757)
        self.image = self.animation.image
        self.image = pygame.transform.scale(self.image, (100, 30))
        self.rect = self.image.get_rect()
        self.flag = False
        self.stop_game_defeat = False

    def update(self):
        if self.flag:
            self.animation.update()
            self.image = pygame.transform.scale(self.animation.image, (100, 30))
            self.flag = False
            if self.animation.image == self.animation.frames[4]:
                self.stop_game_defeat = True
                # экран проигрыша

    def update_game(self):
         return self.stop_game_defeat