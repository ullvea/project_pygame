from classes.base import *


class Kirby(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, confines_sprites):
        super().__init__(groups)
        colorkeys = ((84, 110, 140), (86, 113, 145), (86, 113, 146), (98, 130, 179), (107, 142, 196), (108, 143, 194),
                     (109, 144, 199), (110, 146, 199), (111, 147, 201), (113, 151, 206), (114, 152, 209),
                     (116, 154, 212))

        self.image = load_image('Kirby_character.png', colorkeys)

        self.rect = self.image.get_rect(topleft=pos)
        self.last_rect = self.rect.copy()

        self.standing_animation = load_image('Kirby_character.png', colorkeys)
        self.moving_animation = AnimatedSprite(load_image("moving_animation.png", colorkeys),
                                               4, 1, 76, 16)
        self.start_fly_animation = AnimatedSprite(load_image("Kirby_start_fly.png", colorkeys),
                                                  4, 1, 84, 24)
        self.fly_animation = AnimatedSprite(load_image("Kirby_fly.png", colorkeys),
                                            2, 1, 52, 24)
        self.end_fly_animation = AnimatedSprite(load_image("Kirby_end_fly.png", colorkeys),
                                                2, 1, 52, 24)

        self.orientation = True  # Флаг, отвечающий за направление движения

        # Флаги, отвечающие за то, какую анимацию включать
        self.is_flying = False
        self.is_moving = False
        self.is_standing = True
        self.is_starting_fly = True

        self.obstacle_sprites = obstacle_sprites
        self.confines_sprites = confines_sprites

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.g = 0.25  # чтобы персонаж не мог улетать
        self.jump_speed = -1.5  # чтобы прыжок мог осуществляться, если персонаж на земле
        # минус тк у нас компьютерная сис-ма отсчета
        self.v = 0  # скорость по вертикали

        # Таймер для анимации
        self.animation_timer = 0
        self.animation_delay = 125

    def animation(self):
        ''' Функция отвечает за смену анимации при каком-либо роде действий  '''
        current_time = pygame.time.get_ticks()
        if self.is_flying:
            if current_time - self.animation_timer > self.animation_delay:
                self.image = self.fly_animation.image
                self.fly_animation.update()
                self.animation_timer = current_time  # Сбрасываем таймер
                self.mirror()
        elif self.is_moving:
            self.image = self.moving_animation.image
            self.moving_animation.update()
            self.mirror()
        else:
            self.image = self.standing_animation
            self.mirror()

    def mirror(self):
        if not self.orientation:  # Зеркалим изображение взависимости от направления
            self.image = pygame.transform.flip(self.image, True, False)

    def move(self):
        keys = pygame.key.get_pressed()
        v1 = pygame.math.Vector2(0, 0)

        self.is_standing = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            v1.x -= 1
            self.is_moving = True
            self.orientation = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            v1.x += 1
            self.is_moving = True
            self.orientation = True
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.v = self.jump_speed  # движение вверх
            self.is_flying = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:  # мб анимация подката...
            v1.y += 1
            self.is_moving = False
            self.is_standing = False
        elif keys[pygame.K_SPACE] and self.v == 0:  # Прыжок
            self.v = self.jump_speed  # движение вверх
        else:
            self.is_moving = False
            self.is_standing = True
            self.is_flying = False

        self.direction = v1.normalize() if v1.length() > 0 else v1
        self.rect.x += self.direction.x * self.speed
        self.check_collision('x')
        self.rect.y += self.direction.y * self.speed

        # Гравитация
        self.v += self.g
        self.rect.y += self.v

        self.check_collision('y')

    def check_collision(self, case):
        for item in self.obstacle_sprites:
            if item.rect.colliderect(self.rect):
                if case == 'x':
                    if self.rect.right >= item.rect.left >= self.last_rect.left:
                        self.rect.right = item.rect.left
                    elif self.rect.left <= item.rect.right <= self.last_rect.right:
                        self.rect.left = item.rect.right

                elif case == 'y':
                    if self.rect.bottom >= item.rect.top >= self.last_rect.top:
                        self.rect.bottom = item.rect.top
                        self.v = 0  # сброс скорости тк кирби должна падать вниз
                    elif self.rect.top <= item.rect.bottom <= self.last_rect.bottom:
                        self.rect.top = item.rect.bottom

        for item in self.confines_sprites:
            if self.rect.left > item.rect.left:
                camera.flag = False
                return
            else:
                camera.flag = True

    def update(self):
        self.move()
        self.animation()
        self.last_rect = self.rect.copy()
