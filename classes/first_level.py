from classes.base import *
from classes.kirby import Kirby
from classes.enemies import *


class FirstLevel:
    """Класс, отвечающий за отрисовку и обновление уровня(-ей)"""

    def __init__(self, tmx_map):
        self.surface = pygame.display.get_surface()
        self.can_jump_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()  # группа спрайтов, отвечающая за поверхность (препятствия)
        self.confines_sprites = pygame.sprite.Group()  # группа спрайтов, отвечающая за ограничение камеры
        self.waddle_doo_sprites = pygame.sprite.Group()
        self.tmx(tmx_map)

    def run(self):
        camera.update(self.kirby)
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.update()
        screen.fill((60, 188, 252))
        all_sprites.draw(self.surface)

    def surfx2(self, surf):
        """Функция, увеличивающая размер тайла"""
        return pygame.transform.scale(surf, (TILE_SIZE, TILE_SIZE))

    def tmx(self, tmx_map):
        """Функция, добавляющая cпрайты в группы"""
        for x, y, surf in tmx_map.get_layer_by_name('Surface').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), self.surfx2(surf),
                   (all_sprites, self.obstacle_sprites))

        for x, y, surf in tmx_map.get_layer_by_name('tiles_for_waddle_doo').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), self.surfx2(surf),
                   (self.waddle_doo_sprites, all_sprites))

        for x, y, surf in tmx_map.get_layer_by_name('beautiful_background').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), self.surfx2(surf), all_sprites)

        for x, y, surf in tmx_map.get_layer_by_name('can_jump').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), self.surfx2(surf), (all_sprites, self.can_jump_sprites))

        for x, y, surf in tmx_map.get_layer_by_name('stop_camera').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), self.surfx2(surf),
                   (all_sprites, self.confines_sprites))

        for obj in tmx_map.get_layer_by_name('main'):
            self.kirby = Kirby((obj.x * 2, obj.y * 2),
                               all_sprites, self.obstacle_sprites, self.confines_sprites, self.can_jump_sprites)
            kirby_sprites.add(self.kirby)

        for obj in tmx_map.get_layer_by_name('enemies'):
            if obj.name == 'waddle_doo':
                self.waddle_doo = WaddleDoo((obj.x * 2, obj.y * 2),
                                            all_sprites, self.waddle_doo_sprites, self.obstacle_sprites,
                                            self.kirby)
            """if obj.name == 'fly':
                self.fly = Fly((obj.x * 2, obj.y * 2),
                                                self.all_sprites, self.waddle_doo_sprites, self.obstacle_sprites,
                                                self.kirby)"""