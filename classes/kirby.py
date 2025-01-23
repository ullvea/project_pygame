from classes.base import *


class Kirby(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, confines_sprites):
        super().__init__(groups)
        colorkeys = ((84, 110, 140), (86, 113, 145), (86, 113, 146), (98, 130, 179), (107, 142, 196), (108, 143, 194),
                     (109, 144, 199), (110, 146, 199), (111, 147, 201), (113, 151, 206), (114, 152, 209),
                     (116, 154, 212), (116, 154, 212), (114, 151, 208), (110, 145, 200), (93, 122, 159), (107, 142, 193),
                     (92, 121, 158))

        self.image = load_image('Kirby_character.png', colorkeys)
        self.jump_image = load_image('Kirby_jump.png', colorkeys)

        self.rect = self.image.get_rect(topleft=pos)
        self.last_rect = self.rect.copy()

        self.standing_animation = load_image('Kirby_character.png', colorkeys)
        self.moving_animation = AnimatedSprite(load_image("moving_animation.png", colorkeys),
                                               4, 1, 76, 16)
        self.start_fly_animation = AnimatedSprite(load_image("Kirby_start_fly1.png", colorkeys),
                                                  4, 1, 89, 24)
        self.fly_animation = AnimatedSprite(load_image("Kirby_fly.png", colorkeys),
                                            2, 1, 52, 24)
        self.end_fly_animation = AnimatedSprite(load_image("Kirby_end_fly.png", colorkeys),
                                                4, 1, 92, 24)

        self.orientation = True  # Флаг, отвечающий за направление движения

        # Флаги, отвечающие за то, какую анимацию включать
        self.is_flying = False
        self.is_moving = False
        self.is_standing = True
        self.is_flying_ending = False
        self.is_jumping = True
        self.end_fly = False
        self.is_starting_jumping_animation = False

        self.obstacle_sprites = obstacle_sprites
        self.confines_sprites = confines_sprites

        self.direction = pygame.math.Vector2()
        self.speed = 6
        self.jump_height = -8 # Устанавливаем высоту прыжка

        self.g = 0.5  # чтобы персонаж не мог улетать
        self.v = 0  # скорость по вертикали

        self.jump_time = 1000  # Длительность прыжка

        # Таймеры для анимации
        self.animation_timer = 0
        self.animation_delay = 100
        self.animation_delay_fly = 75
        self.extra_animation_timer = self.animation_delay_fly * len(self.start_fly_animation.frames)
        self.extra_animation_timer2 = self.animation_delay_fly * len(self.end_fly_animation.frames)

    def animation(self):
        ''' Функция отвечает за смену анимации при каком-либо роде действий  '''
        current_time = pygame.time.get_ticks()
        if self.is_flying and not self.is_jumping:
            if self.extra_animation_timer > current_time:
                if current_time - self.animation_timer > self.animation_delay_fly:
                    self.image = self.start_fly_animation.image
                    self.start_fly_animation.update()
                    self.animation_timer = current_time  # Сбрасываем таймер
                    self.mirror()
            elif current_time - self.animation_timer > self.animation_delay:
                self.image = self.fly_animation.image
                self.fly_animation.update()
                self.animation_timer = current_time  # Сбрасываем таймер
                self.mirror()
            self.end_fly = True
            self.end_fly_animation.image = self.end_fly_animation.frames[0]


        else:
            self.start_fly_animation.image = self.start_fly_animation.frames[0]
            self.extra_animation_timer = self.animation_delay_fly * len(
                self.start_fly_animation.frames) + current_time

            if self.end_fly:
                if self.extra_animation_timer > current_time:
                    if current_time - self.animation_timer > self.animation_delay_fly:
                        self.image = self.end_fly_animation.image
                        self.end_fly_animation.update()
                        if self.image == self.end_fly_animation.frames[3]:
                            self.end_fly = False
                        self.animation_timer = current_time  # Сбрасываем таймер
                        self.mirror()
            elif self.is_starting_jumping_animation:
                self.image = self.jump_image
                self.mirror()
            elif self.is_moving:
                self.image = self.moving_animation.image
                self.moving_animation.update()
                self.mirror()
            else:
                self.image = self.standing_animation
                self.mirror()

    def mirror(self):
        """Функция, отвечающая за отзеркаливание изображения"""
        if not self.orientation:  # Зеркалим изображение взависимости от направления
            self.image = pygame.transform.flip(self.image, True, False)

    def move(self):
        keys = pygame.key.get_pressed()
        v1 = pygame.math.Vector2(0, 0)
        print(self.v)

        self.is_standing = False
        current_time = pygame.time.get_ticks()
        if not self.is_jumping:
            self.jump_time = current_time + 1000

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            v1.x -= 1
            self.is_moving = True
            self.orientation = False
            self.is_starting_jumping_animation = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            v1.x += 1
            self.is_moving = True
            self.orientation = True
            self.is_starting_jumping_animation = False
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.is_jumping:
                self.rect.y += self.jump_height
                if self.orientation:
                    self.rect.x += 1
                else:
                    self.rect.x -= 1
                self.is_starting_jumping_animation = True
                if self.jump_time - current_time <= 0:
                    self.is_jumping = False
                    self.jump_time = current_time + 1000
                    self.v = 0
                    print('Jump!')
            else:
                self.v -= 1
                self.is_flying = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:  # мб анимация АТАКИИ...
            v1.y += 1
            self.is_moving = False
            self.is_standing = False
        else:
            self.is_moving = False
            self.is_standing = True
            self.is_flying = False
            self.is_starting_jumping_animation = False


        self.direction = v1.normalize() if v1.length() > 0 else v1
        # Вектор надо нормализовывать, чтобы скорость была единичной
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
                if self.v >= 0:
                    self.is_jumping = True
                if case == 'x':
                    if self.rect.right >= item.rect.left >= self.last_rect.left:
                        self.rect.right = item.rect.left
                    elif self.rect.left <= item.rect.right <= self.last_rect.right:
                        self.rect.left = item.rect.right

                elif case == 'y':
                    if self.rect.bottom >= item.rect.top >= self.last_rect.top:
                        self.rect.bottom = item.rect.top
                    elif self.rect.top <= item.rect.bottom <= self.last_rect.bottom:
                        self.rect.top = item.rect.bottom
                    self.v = 0  # сброс скорости тк кирби должна падать вниз

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
