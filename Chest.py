import pygame
from config import *
from Characters import NPC

class Chest(NPC):
    def __init__(self, game, scene, group, pos, z, name):
        super().__init__(game, scene, group, pos, z, name)
        self.state= Idle(self)

    def update(self, dt):
        self.state.update_state(dt, self)

class Idle:
    def __init__(self, chest):
        chest.frame_index=0

    def update_state(self, dt, chest):
        chest.animate(f'idle_left',  dt)
