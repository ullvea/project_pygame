from classes.base import *
import math


class WaddleDoo(pygame.sprite.Sprite):
    def __init__(self, pos, groups, waddle_doo_sprites, obstacle_sprites, player):
        super().__init__(groups)
        self.colorkeys = [(98, 130, 179), (116, 154, 212), (111, 147, 201), (84, 110, 140)]
        self.image = load_image('waddle_doo.png', self.colorkeys)
        self.attack_image = load_image('waddle_doo_attack.png', self.colorkeys)
        self.animation = AnimatedSprite(load_image('waddle_doo.png', self.colorkeys), 2, 1, 36, 16)
        self.animation_is_attacking = AnimatedSprite(load_image('waddle_doo_is_attacked.png', self.colorkeys),
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
        self.extra_animation_timer = 600
        self.animation_delay = 100
        self.speed = -3  # Скорость отрицательная, так как у нас компьютерная система отсчёта
        self.v = 0
        self.g = 0.2
        self.shot = None

    def attack(self):
        current_time = pygame.time.get_ticks()
        distance = math.sqrt((self.rect.centerx - self.player.rect.centerx) ** 2 +
                             (self.rect.centery - self.player.rect.centery) ** 2)

        if distance <= 220 and ((self.rect.x > self.player.rect.x and self.orientation) or
        (self.rect.x < self.player.rect.x and not self.orientation)):  # Cоздание атаки
            if current_time - self.animation_timer_for_shots > 2000:
                self.attacking = True
                for i in range(4, 1, -1):
                    if self.orientation:
                        x = self.rect.x - (i - 1) * 18
                    else:
                        x = self.rect.x + (i - 1) * 18
                    y = self.rect.y - (i - 1) * 17
                    speed = [self.speed, self.speed - 2 * i]
                    self.shot = Shot(load_image('waddle_doo_attack.png', self.colorkeys), x, y, speed,
                                     self.orientation)
                    self.animation_timer_for_shots = current_time


        for item in sprite_shots_group:  # Выстрелы должны удалятся при столкновении с Кирби
            if pygame.sprite.spritecollideany(item, kirby_sprites):
                item.kill()

    def move(self):
        self.rect.x += self.speed
        self.check_collisions('x')

        collided_sprite = pygame.sprite.spritecollideany(self, self.waddle_doo_sprites)
        if collided_sprite:
            self.orientation = not self.orientation
            self.speed *= -1

        if self.orientation:
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed
        # Гравитация
        self.v += self.g
        self.rect.y += self.v
        self.check_collisions('y')

    def check_collisions(self, case):
        for item in self.obstacle_sprites:
            if item.rect.colliderect(self.rect):
                if case == 'y':
                    if self.rect.bottom >= item.rect.top >= self.last_rect.top:
                        self.rect.bottom = item.rect.top
                    elif self.rect.top <= item.rect.bottom <= self.last_rect.bottom:
                        self.rect.top = item.rect.bottom
                    self.v = 0

    def mirror(self):
        """Функция, отвечающая за отзеркаливание изображения"""
        if not self.orientation:  # Зеркалим изображение
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.move()
        self.attack()
        current_time = pygame.time.get_ticks()
        self.last_rect = self.rect.copy()

        if current_time - self.animation_timer > self.animation_delay:
            if not self.attacking:
                self.image = self.animation.image
                self.animation.update()
                self.extra_animation_timer = current_time + 600
            else:
                if self.extra_animation_timer > current_time:
                    if current_time - self.animation_timer > self.animation_delay:
                        self.image = self.animation_is_attacking.image
                        self.animation_is_attacking.update()
                else:
                    self.attacking = False
            self.animation_timer = current_time
            self.mirror()



class Shot(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed, orientation):
        super().__init__(all_sprites, sprite_shots_group)
        self.image = image
        self.orientation = orientation
        self.speed_x = speed[0]
        self.speed_y = speed[1]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.current_time = pygame.time.get_ticks()
        self.start_moving = True # Флаг, отвечающий за то, чтобы вначале выстрелы пролетали вперед, а затем начинали падать

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.current_time < 600 and self.start_moving:  # Выстрел должен пропасть через определенное кол-во времени
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.current_time = now
            self.start_moving = False
        elif now - self.current_time < 400:
            self.rect.x += self.speed_x
            if not self.orientation:
                self.rect.y -= self.speed_y - self.speed_x * 2
            else:
                self.rect.y -= self.speed_y
        else:
            self.kill()
