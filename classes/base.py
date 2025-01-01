import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # Чтобы не писало "Hello from pygame..."
import pygame
import sys
from pytmx import *

size = width, height = 768,  240  # 768, 240
screen = pygame.display.set_mode((width, height))
ANIMATION_SPEED = 6
fps = 60
TILE_SIZE = 8

obstacles = pygame.sprite.Group()  # препятствия с англ


def load_image(name, colorkey=None):  # Функция для зaгрузки изображений
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Sprite(pygame.sprite.Sprite):
    '''класс, отвечающий за отрисовку спрайтов на уровне для удобства разработчика'''

    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill('white')
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
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)
