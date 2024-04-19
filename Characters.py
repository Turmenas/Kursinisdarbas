import pygame
from config import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, game, scene, group, pos, z, name):
        super().__init__(group)

        self.game = game
        self.scene = scene
        self.z = z
        self.name = name
        self.import_images(f'assets/characters/{self.name}/')
        self.frame_index = 0
        self.image = self.animations['idle_left'][self.frame_index].convert_alpha()
        self.rect = self.image.get_frect(topleft = pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width/2, -self.rect.height/2)
        self.speed = 80
        self.force = 2000
        self.acc = vec()
        self.vel = vec()
        self.frict = -15

    def import_images(self, path):
        self.animations = self.game.get_animations(path)

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = self.game.get_images(full_path)

    def animate(self, state, fps, loop=True):
        self.frame_index += fps

        if self.frame_index >= len(self.animations[state])-1:
            if loop:
                self.frame_index = 0
            else:
                self.frame_index = len(self.animations[state])-1

        self.image = self.animations[state][int(self.frame_index)]

    def get_collision_list(self, group):
        collision_list = pygame.sprite.spritecollide(self, group, False)
        return collision_list

    def collisions(self, axis, group):
        for sprite in self.get_collision_list(group):
            if self.hitbox.colliderect(sprite.hitbox):
                if axis == 'x':
                    if self.vel.x >= 0: self.hitbox.right = sprite.hitbox.left
                    if self.vel.x <= 0: self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                if axis == 'y':
                    if self.vel.y >= 0: self.hitbox.bottom = sprite.hitbox.top
                    if self.vel.y <= 0: self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery

    def physics(self, dt):
        self.acc.x += self.vel.x *self.frict
        self.vel.x += self.acc.x *dt
        self.hitbox.centerx += self.vel.x * dt + (self.vel.x/2 * dt)
        self.rect.centerx = self.hitbox.centerx
        self.collisions('x', self.scene.block_sprites)

        self.acc.y += self.vel.y * self.frict
        self.vel.y += self.acc.y * dt
        self.hitbox.centery += self.vel.y * dt + (self.vel.y / 2 * dt)
        self.rect.centery = self.hitbox.centery
        self.collisions('y', self.scene.block_sprites)

        if self.vel.magnitude() > self.speed:
            self.vel = self.vel.normalize() * self.speed

    def Update(self, dt):
        self.physics(dt)
        self.animate('idle_right', 15 * dt )

class Player(NPC):
    def __init__(self, game, scene, group, pos, z, name):
        super().__init__(game, scene, group, pos, z, name)

    def move(self):
        if INPUTS['a']:
            self.acc.x = -self.force
        elif INPUTS['d']:
            self.acc.x = self.force
        else:
            self.acc.x = 0

        if INPUTS['w']:
            self.acc.y = -self.force
        elif INPUTS['s']:
            self.acc.y = self.force
        else:
            self.acc.y = 0

    def update(self, dt):
        self.physics(dt)
        self.move()
        self.animate('idle_right', 3 * dt)