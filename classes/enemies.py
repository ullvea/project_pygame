from classes.base import *
import math


class WaddleDoo(pygame.sprite.Sprite):
    def __init__(self, pos, groups, waddle_doo_sprites, obstacle_sprites, player):
        super().__init__(groups)
        colorkeys = [(98, 130, 179), (116, 154, 212), (111, 147, 201), (84, 110, 140)]
        self.image = load_image('waddle_doo.png', colorkeys)
        self.attack_image = load_image('waddle_doo_attack.png', colorkeys)
        self.animation = AnimatedSprite(load_image('waddle_doo.png', colorkeys), 2, 1, 36, 16)
        self.animation_is_attacked = AnimatedSprite(load_image('waddle_doo.png', colorkeys),
                                                    2, 1, 36, 16)
        self.rect = self.image.get_rect(topleft=pos)

        self.waddle_doo_sprites = waddle_doo_sprites
        self.obstacle_sprites = obstacle_sprites

        self.attacking = False
        self.player = player

        # Таймер для анимации
        self.animation_timer = 0
        self.animation_delay = 125
        self.speed = -2 # Скорость отрицательная, так как у нас компьютерная система отсчёта

    def move(self):
        # Двигаем персонажа
        self.rect.x += self.speed
        collided_sprite = pygame.sprite.spritecollideany(self, self.waddle_doo_sprites)
        if collided_sprite:
            self.rect.bottom = collided_sprite.rect.top
        if not pygame.sprite.spritecollideany(self, self.obstacle_sprites):
            self.rect.y += 3

    def attack(self):
        distance = math.sqrt((self.rect.centerx - self.player.rect.centerx) ** 2 +
                             (self.rect.centery - self.player.rect.centery) ** 2)
        if distance <= 220:
            pass



    def update(self):
        self.move()
        self.attack()
        current_time = pygame.time.get_ticks()

        if current_time - self.animation_timer > self.animation_delay:
            self.image = self.animation.image
            self.animation.update()
            self.animation_timer = current_time


