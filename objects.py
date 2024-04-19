import pygame
from config import *

class Object(pygame.sprite.Sprite):
    def __init__ (self, groups, pos, z='blocks', surf=pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.hitbox = self.rect.copy().inflate(0, 0)
        self.z = z