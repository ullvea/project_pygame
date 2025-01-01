from base import *
from kirby import Kirby

class FirstLevel:
    def __init__(self, tmx_map):
        self.surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.camera = Camera()
        self.tmx(tmx_map)

    def run(self):
        image = load_image("Mushroom_Forest_Zone_Layout_now.png")
        screen.blit(image,(0,0))
        #self.camera.update(self.kirby)
        #for sprite in self.all_sprites:
            #self.camera.apply(sprite)
        self.all_sprites.update()
        self.all_sprites.draw(self.surface)

    def tmx(self, tmx_map):
        '''функция, добавляющая cпрайты в группу'''
        for x, y, surf in tmx_map.get_layer_by_name('Surface').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites, self.obstacle_sprites))

        for obj in tmx_map.get_layer_by_name('main'):
            self.kirby = Kirby((obj.x // 4, obj.y // 4), self.all_sprites, self.obstacle_sprites)
