from classes.base import *


class WaddleDoo(pygame.sprite.Sprite):
    def __init__(self, pos, groups, waddle_doo_sprites):
        super().__init__(groups)
        colorkeys = [(98, 130, 179), (116, 154, 212), (111, 147, 201), (84, 110, 140)]
        self.image = load_image('waddle_doo.png', colorkeys)
        self.animation = AnimatedSprite(load_image('waddle_doo.png', colorkeys), 2, 1, 36, 16)
        self.rect = self.image.get_rect(topleft=pos)
        self.waddle_doo_sprites = waddle_doo_sprites

        # Таймер для анимации
        self.animation_timer = 0
        self.animation_delay = 125
        self.speed = 2
        self.orientation = 1

    def move(self):
        # Двигаем персонажа
        self.rect.x += self.orientation * self.speed
        if pygame.sprite.spritecollideany(self, self.waddle_doo_sprites):
            self.orientation *= -1


    def update(self):
        self.move()
        current_time = pygame.time.get_ticks()

        if current_time - self.animation_timer > self.animation_delay:
            self.image = self.animation.image
            self.animation.update()
            self.animation_timer = current_time

            if self.orientation > 0:  # Зеркалим изображение в зависимости от направления
                self.image = pygame.transform.flip(self.image, True, False)


