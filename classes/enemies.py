from classes.base import *
import math


class WaddleDoo(pygame.sprite.Sprite):
    def __init__(self, pos, groups, waddle_doo_sprites, obstacle_sprites, player):
        super().__init__(groups)
        self.colorkeys = [(98, 130, 179), (116, 154, 212), (111, 147, 201), (84, 110, 140)]
        self.image = load_image('waddle_doo.png', self.colorkeys)
        self.attack_image = load_image('waddle_doo_attack.png', self.colorkeys)
        self.animation = AnimatedSprite(load_image('waddle_doo.png', self.colorkeys), 2, 1, 36, 16)
        self.animation_is_attacked = AnimatedSprite(load_image('waddle_doo.png', self.colorkeys),
                                                    2, 1, 36, 16)
        self.rect = self.image.get_rect(topleft=pos)
        self.last_rect = self.rect.copy()
        self.waddle_doo_sprites = waddle_doo_sprites
        self.obstacle_sprites = obstacle_sprites

        self.attacking = False
        self.player = player
        self.orientation = True

        # Таймер для анимации
        self.animation_timer = 0
        self.animation_timer_for_shots = 0
        self.animation_delay = 100
        self.speed = -3  # Скорость отрицательная, так как у нас компьютерная система отсчёта
        self.v = 0
        self.g = 0.2
        self.shot = Shot(load_image('waddle_doo_attack.png', self.colorkeys), self)

    def attack(self):
        current_time = pygame.time.get_ticks()
        distance = math.sqrt((self.rect.centerx - self.player.rect.centerx) ** 2 +
                             (self.rect.centery - self.player.rect.centery) ** 2)
        if distance <= 320 and self.rect.x > self.player.rect.x: # Cоздание атаки
            for i in range(5):
                if current_time - self.animation_timer_for_shots > 250:
                    self.shot = Shot(load_image('waddle_doo_attack.png', self.colorkeys), self)
                    self.animation_timer_for_shots = current_time

        for item in sprite_shots_group:  # Выстрелы должны удалятся при столкновении с Кирби
            if pygame.sprite.spritecollideany(item, kirby_sprites):
                item.kill()
                print('Kill!')

    def move(self):
        self.rect.x += self.speed
        collided_sprite = pygame.sprite.spritecollideany(self, self.waddle_doo_sprites)
        if collided_sprite:
            self.orientation = not self.orientation
            self.speed *= -1

        for item in self.obstacle_sprites:
            if item.rect.colliderect(self.rect):
                self.rect.y -= 32
        if self.orientation:
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed
        # Гравитация
        self.v += self.g
        self.rect.y += self.v

        for item in self.obstacle_sprites:
            if item.rect.colliderect(self.rect):
                if self.rect.bottom >= item.rect.top >= self.last_rect.top:
                    self.rect.bottom = item.rect.top
                elif self.rect.top <= item.rect.bottom <= self.last_rect.bottom:
                    self.rect.top = item.rect.bottom
                self.v = 0

    def mirror(self):
        """Функция, отвечающая за отзеркаливание изображения"""
        if not self.orientation:  # Зеркалим изображение взависимости о
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.move()
        self.attack()
        current_time = pygame.time.get_ticks()
        self.last_rect = self.rect.copy()

        if current_time - self.animation_timer > self.animation_delay:
            self.image = self.animation.image
            self.animation.update()
            self.animation_timer = current_time
            self.mirror()


class Shot(pygame.sprite.Sprite):
    def __init__(self, image, enemy):
        super().__init__(all_sprites, sprite_shots_group)
        self.image = image
        self.rect = self.image.get_rect(topleft=(enemy.rect.x, enemy.rect.y))
        self.current_time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.current_time > 100: # Выстрел должен пропасть через определенное кол-во времени
            print('Kill by himself')
            self.kill()
