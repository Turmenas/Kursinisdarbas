import random
import pygame
from config import *
from Characters import NPC


class Enemy(NPC):
    def __init__(self, game, scene, group, pos, z, name):
        super().__init__(game, scene, group, pos, z, name)
        self.state = Move(self)
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.speed = 5
        self.hitbox = self.rect.copy().inflate(-self.rect.width/2, -self.rect.height/2)
        self.stuck_timer = 0
        self.change_direction_interval = 3

    def get_direction(self):
        unblocked_directions = self.get_unblocked_directions()
        if self.stuck_timer > self.change_direction_interval:
            self.stuck_timer = 0
            return random.choice(unblocked_directions) if unblocked_directions else self.direction
        return random.choice(unblocked_directions) if unblocked_directions else None

    def update(self, dt):
        self.stuck_timer += dt
        self.change_state()
        self.state.update_state(dt, self)

class Idle:
    def __init__(self, enemy):
        enemy.frame_index = 0

    def enter_state(self, enemy):
            return Move(enemy)

    def update_state(self, dt, enemy):
        enemy.animate(f'idle_{enemy.get_direction()}', 2 * dt)
        enemy.movement()
        enemy.physics(dt, enemy.frict)

class Move:
    def __init__(self, enemy):
        Idle.__init__(self, enemy)
        self.max_travel = random.randint(1, 8)
        self.movement_loop = 1

    def enter_state(self, enemy):
        if self.max_travel <= 0 or enemy.vel.magnitude() < 1:
            enemy.direction = enemy.get_direction()
            return Idle(enemy)

        # if enemy.check_player_collision():
            # return Death(enemy)

    def update_state(self, dt, enemy):
        self.max_travel -= dt
        if self.max_travel > 0:
            enemy.move[f'{enemy.direction}'] = True
        enemy.animate(f'move_{enemy.direction}', dt)
        enemy.movement()
        enemy.physics(dt, enemy.frict)
