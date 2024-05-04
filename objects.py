import pygame
from config import *

class Collider(pygame.sprite.Sprite):
    def __init__ (self, groups, pos, size, number):
        super().__init__(groups)

        self.image = pygame.Surface(size)
        self.rect = self.image.get_frect(topleft = pos)
        self.number = number

class Object(pygame.sprite.Sprite):
    def __init__ (self, groups, pos, z='blocks', surf=pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.hitbox = self.rect.copy().inflate(0, 0)
        self.z = z

class Wall(Object):
    def __init__(self, groups, pos, z, surf):
        super().__init__(groups, pos, z, surf)

        self.hitbox = self.rect.copy().inflate(0, -self.rect.height/2)

class Barrier(Object):
    def __init__(self, groups, pos, z, surf):
        super().__init__(groups, pos, z, surf)

        self.hitbox = self.rect.copy().inflate(0, 0)

class Background(Object):
    def __init__(self, groups, pos, z, surf):
        super().__init__(groups, pos, z, surf)

        self.hitbox = self.rect.copy().inflate(-self.rect.width, -self.rect.height)