import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # Чтобы не писало "Hello from pygame..."
import pygame
import sys
from pytmx import *

size = width, height = 700, 525
screen = pygame.display.set_mode((width, height))
fps = 30
TILE_SIZE = 16


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
    def __init__(self, flag=True):
        self.dx = 0
        self.dy = 0
        self.flag = flag

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        if self.flag:
            obj.rect.x += self.dx
            obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 8 - width // 8)
        self.dy = -(target.rect.y + target.rect.h // 1.5 - height // 1.5)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(animated_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.animation_complete = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def is_finished(self):
        return self.animation_complete


obstacles = pygame.sprite.Group()
animated_sprites = pygame.sprite.Group()
camera = Camera()


def load_image(name, colorkeys=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname).convert_alpha()  # Загружаем изображение с альфа-каналом
    if colorkeys:
        width_im, height_im = image.get_size()
        pixels = pygame.surfarray.pixels3d(image)  # Привязка пикселей к 3D-массиву
        # Проходим по всем пикселям и заменяем указанные цвета на прозрачные
        for x in range(width_im):
            for y in range(height_im):
                if tuple(pixels[x][y]) in colorkeys:
                    # Устанавливаем альфа-канал в 0 (прозрачный)
                    image.set_at((x, y), (0, 0, 0, 0))  # RGBA: (R, G, B, A)
    return image
