import os
import sys
import random
import pygame

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Bomb.image
        self.image_boom = load_image("boom.png")
        self.rect = self.image.get_rect()
        self.image_width, self.image_height = self.rect.width, self.rect.height
        self.rect.x, self.rect.y = random.randrange(0, width - self.image_width),\
                                   random.randrange(0, height - self.image_height)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = self.image_boom


all_sprites = pygame.sprite.Group()

for i in range(20):
    bomb = Bomb(all_sprites)

if __name__ == '__main__':
    running = True
    fps = 60
    clock = pygame.time.Clock()
    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            all_sprites.update(event)
            if event.type == pygame.QUIT:
                running = False
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
