import pygame
from config import *
from Characters import NPC

class Player(NPC):
    def __init__(self, game, scene, group, pos, z, name):
        super().__init__(game, scene, group, pos, z, name)

        self.state = Idle(self)

    def movement(self):
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

    def vec_to_mouse(self, speed):
        direction = vec(pygame.mouse.get_pos()) - (vec(self.rect.center)-vec(self.scene.camera.offset))
        if direction.length() > 0:
            direction.normalize_ip()
            return direction*speed


class Idle:
    def __init__(self, character):
        character.frame_index=0

    def enter_state(self, character):
        if character.vel.magnitude() > 1:
            return Move(character)

        if INPUTS['right_click']:
            return Dodge(character)

    def update_state(self, dt, character):
        character.animate(f'idle_{character.get_direction()}', 2 * dt)
        character.movement()
        character.physics(dt, character.frict)


class Move:
    def __init__(self, character):
        Idle.__init__(self, character)

    def enter_state(self, character):
        if character.vel.magnitude() < 1:
            return Idle(character)

        if INPUTS['right_click']:
            return Dodge(character)

    def update_state(self, dt, character):
        character.animate(f'move_{character.get_direction()}', 3 * dt)
        character.movement()
        character.physics(dt, character.frict)


class Dodge:
    def __init__(self, character):
        Idle.__init__(self, character)
        INPUTS['right_click'] = False
        self.timer = 2
        self.dodge_pending = False
        self.vel = character.vec_to_mouse(300)

    def enter_state(self, character):
        if INPUTS['right_click']:
            self.dodge_pending = True
        if self.timer <= 0:
            if self.dodge_pending:
                return Dodge(character)
            else:
                return Idle(character)

    def update_state(self, dt, character):
        self.timer -= dt
        character.animate(f'dodge', 5 * dt)
        character.physics(dt, -2)
        character.acc = vec()
        character.vel = self.vel