import pygame
from Setting import *


class Background(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        bg_image = pygame.image.load('graphics/ground.png')

        full_width = bg_image.get_width()
        full_height = bg_image.get_height()

        self.image = pygame.Surface((full_width * 2), full_width)
        self.image.blit(bg_image, (0, 0))
        self.image.blit(bg_image, (full_width, 0))

        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = self.rect.x

    def update(self, dt):
        self.pos.x = -300 * dt
        if self.rect.center <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)
