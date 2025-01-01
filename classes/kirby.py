from classes.base import *


class Kirby(pygame.sprite.Sprite):
    '''класс, отвечающий за отрисовку спрайтов на уровне для удобства разработчика'''

    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill('pink')
        self.rect = self.image.get_rect(topleft=pos)
        self.last_rect = self.rect.copy()
        self.obstacle_sprites = obstacle_sprites

        self.direction = pygame.math.Vector2()
        self.speed = 1

        self.g = 0.25 # чтобы персонаж не мог улетать
        self.jump_speed = -3 # чтобы прыжок мог осуществляться если перс на земле
        # минус тк у нас компьютерная сис-ма отсчета
        self.v = 0 # (СКОРОСТЬ ПО ВЕРТ)

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
                        self.v = 0 # сброс скорости тк кирби должна падать вниз
                    elif self.rect.top <= item.rect.bottom <= self.last_rect.bottom:
                        self.rect.top = item.rect.bottom


    def move(self):
        keys = pygame.key.get_pressed()
        v1 = pygame.math.Vector2(0, 0)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            v1.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            v1.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            v1.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            v1.y += 1

        self.direction = v1.normalize() if v1.length() > 0 else v1
        self.rect.x += self.direction.x * self.speed
        self.check_collision('x')
        self.rect.y += self.direction.y * self.speed

        # Гравитация
        self.v += self.g
        self.rect.y += self.v

        self.check_collision('y')

        if keys[pygame.K_SPACE] and self.v == 0:
            self.v = self.jump_speed # движение вверх

    def update(self):
        self.move()
        self.last_rect = self.rect.copy()
