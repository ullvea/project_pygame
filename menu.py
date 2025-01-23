from classes.base import *


# Класс кнопки
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = pygame.Color('purple')
        self.hovered = False

    def draw(self, surface):
        # Изменение цвета при наведении курсора
        if self.hovered:
            pygame.draw.rect(surface, pygame.Color('pink'), self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        # заменить шрифт: comicsansms
        font = pygame.font.Font('1stenterprises3D.ttf', 30)
        text_surface = font.render(self.text, True, pygame.Color('white'))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def event(self, event):
        if event.type == pygame.MOUSEMOTION:
            # Проверка на наведение курсора
            self.hovered = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия кнопки мыши
            if self.hovered:
                print("игра началась :)")


def main_menu():
    pygame.init()
    # print(pygame.font.get_fonts())
    pygame.display.set_caption("Menu")
    back_ground = load_image("pink_wallpaper.jpg")
    # изменяем размер картинки
    back_ground = pygame.transform.scale(back_ground, (700, 525))
    screen.fill((255, 255, 255))
    running = True

    play_button = Button(50, 60, 100, 50, "PLAY")

    image = load_image("yellow_cursor2.png")

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            screen.blit(back_ground, (0, 0))
            # отрисовка кнопки
            play_button.draw(screen)
            if pygame.mouse.get_focused():
                x, y = pygame.mouse.get_pos()
                # изображение курсора
                screen.blit(image, (x, y))

            # play_button.draw(screen)
            pygame.mouse.set_visible(False)

            play_button.event(event)

        pygame.display.flip()
    pygame.quit()


main_menu()
