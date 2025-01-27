import os
import pygame
import sys
from pytmx import *

size = WIDTH, HEIGHT = 700, 525
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 25
TILE_SIZE = 32


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
        self.dx = -(target.rect.x + target.rect.w // 8 - WIDTH // 8)
        self.dy = -(target.rect.y + target.rect.h // 1.5 - HEIGHT // 1.5)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(animated_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

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



# Класс кнопки
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = pygame.Color('red')
        self.hovered = False
        self.sound = pygame.mixer.Sound('sound\\btn_click.mp3')

    def draw(self, surface):
        # Изменение цвета при наведении курсора
        if self.hovered:
            pygame.draw.rect(surface, pygame.Color('pink'), self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        # заменить шрифт: comicsansms
        font = pygame.font.Font('font.ttf', 30)
        text_surface = font.render(self.text, True, pygame.Color('white'))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def event(self, event):
        if event.type == pygame.MOUSEMOTION:
            # Проверка на наведение курсора
            self.hovered = self.rect.collidepoint(event.pos)



class ImageButton:
    def __init__(self,  pos, image, hovered_image):
        self.normal_image = load_image(image, [], 1)
        self.image = self.normal_image
        self.rect = self.image.get_rect(topleft=pos)
        self.hovered_image = load_image(hovered_image, [], 1)
        self.hovered = False

    def draw(self):
        # Изменение цвета при наведении курсора
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.hovered_image
        else:
            self.image = self.normal_image
        screen.blit(self.image, self.rect.topleft)


obstacles = pygame.sprite.Group()
animated_sprites = pygame.sprite.Group()
sprite_shots_group = pygame.sprite.Group()
kirby_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
objects_sprites = pygame.sprite.Group()
damage_sprites = pygame.sprite.Group()
camera = Camera()


def load_image(name, colorkeys=None, scale=2):
    '''Функция для загрузки изображений с обесцвечиванием нескольких цветов'''
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)  # Загружаем изображение
    width, height = image.get_size()
    image = pygame.transform.scale(image, (width * scale, height * scale))  # Меняем размеры изображения
    image = image.convert_alpha()  # Загружаем изображение с альфа-каналом
    if colorkeys:
        width_im, height_im = image.get_size()
        pixels = pygame.surfarray.pixels3d(image)  # Привязка пикселей к 3D-массиву
        for x in range(width_im):
            for y in range(height_im):
                if tuple(pixels[x][y]) in colorkeys:
                    # Делаем альфа-канал в прозрачным
                    image.set_at((x, y), (0, 0, 0, 0))  # RGBA: (R, G, B, A)
    return image
