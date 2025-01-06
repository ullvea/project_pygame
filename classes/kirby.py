from classes.base import *


class Kirby(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, confines_sprites):
        super().__init__(groups)

        self.image = load_image('Kirby_character.png',
                                [(98, 130, 179), (116, 154, 212), (111, 147, 201)])
        self.rect = self.image.get_rect(topleft=pos)
        self.last_rect = self.rect.copy()

        self.moving_animation = AnimatedSprite(load_image("moving_animation.png", [(98, 130, 179),
                                                                                   (116, 154, 212), (111, 147, 201),
                                                                                   (84, 110, 140)]),
                                               4, 1, 76, 16)
        self.standing_animation = load_image('Kirby_character.png',
                                [(98, 130, 179), (116, 154, 212), (111, 147, 201)])

        self.is_moving = False
        self.is_standing = True

        self.obstacle_sprites = obstacle_sprites
        self.confines_sprites = confines_sprites

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.g = 0.25  # чтобы персонаж не мог улетать
        self.jump_speed = -3  # чтобы прыжок мог осуществляться, если персонаж на земле
        # минус тк у нас компьютерная сис-ма отсчета
        self.v = 0  # СКОРОСТЬ ПО ВЕРТКАЛИ


    def animation(self):
        '''Функция отвечает за смену анимации при каком-либо роде действий'''
        if self.is_moving:
            self.image = self.moving_animation.image
            self.moving_animation.update()
        else:
            self.image = self.standing_animation


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


    def move(self):
        keys = pygame.key.get_pressed()
        v1 = pygame.math.Vector2(0, 0)

        self.is_moving = True
        self.is_standing = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            v1.x -= 1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            v1.x += 1
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            v1.y -= 1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            v1.y += 1
        elif keys[pygame.K_SPACE] and self.v == 0:
            self.v = self.jump_speed  # движение вверх
        else:
            self.is_moving = False
            self.is_standing = True

        self.direction = v1.normalize() if v1.length() > 0 else v1
        self.rect.x += self.direction.x * self.speed
        self.check_collision('x')
        self.rect.y += self.direction.y * self.speed

        # Гравитация
        self.v += self.g
        self.rect.y += self.v

        self.check_collision('y')


    def update(self):
        self.move()
        self.animation()
        self.last_rect = self.rect.copy()
