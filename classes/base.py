import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # Чтобы не писало "Hello from pygame..."
import pygame
import sys
from pytmx import *

size = width, height = 700,  300  # 768, 240
screen = pygame.display.set_mode((width, height))
screen.fill((255,0,0))
ANIMATION_SPEED = 6
fps = 60
TILE_SIZE = 16

obstacles = pygame.sprite.Group()  # препятствия с англ


def load_image(name, colorkeys=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname).convert_alpha()  # Загружаем изображение с альфа-каналом
    if colorkeys:
        width_im, height_im = image.get_size()
        pixels = pygame.surfarray.pixels3d(image)
        # Проходим по всем пикселям и заменяем указанные цвета на прозрачные
        for x in range(width_im):
            for y in range(height_im):
                if tuple(pixels[x][y]) in colorkeys:
                    # Устанавливаем альфа-канал в 0 (прозрачный)
                    image.set_at((x, y), (0, 0, 0, 0))  # RGBA: (R, G, B, A)
    return image


class Sprite(pygame.sprite.Sprite):
    '''класс, отвечающий за отрисовку спрайтов на уровне для удобства разработчика'''

    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 8 - width // 8)
        self.dy = -(target.rect.y + target.rect.h // 1.5 - height // 1.5)
