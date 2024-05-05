import pygame
from config import *
from camera import Camera
from Characters import NPC
from Player import Player
from Chest import Chest
from Enemy import Enemy
from objects import *
from pytmx.util_pygame import  load_pygame
from abc import ABC, abstractmethod


class State(ABC):
    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def enter_state(self):
        if len(self.game.states) < 1:
            self.prev_state = self.game.states[-1]
        self.game.states.append(self)

    def exit_state(self):
        self.game.states.pop()

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

class TitleScreen(State):
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, dt):
        if INPUTS['space']:
            Scene(self.game, '0', '0').enter_state()
            self.game.reset_inputs()

    def draw(self, screen):
        screen.fill(COLORS['black'])
        self.game.render_text('Press space to play', COLORS['white'], self.game.font, (WIDTH/2, HEIGHT/2), centered=True)

class EndScreen(State):
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, dt):
        if INPUTS['space']:
            self.game.running = False

    def draw(self, screen):
        screen.fill(COLORS['black'])
        self.game.render_text('You got the treasure, press space to quit', COLORS['white'], self.game.font, (WIDTH/2, HEIGHT/2), centered=True)

class Scene(State):
    def __init__(self, game, current_scene, entry_point):
        State.__init__(self, game)
        self.current_scene = current_scene
        self.entry_point = entry_point

        self.camera = Camera(self)
        self.update_sprites = pygame.sprite.Group()
        self.drawn_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.exit_sprites = pygame.sprite.Group()

        self.tmx_data = load_pygame(f'scenes/{self.current_scene}/{self.current_scene}.tmx')
        self.create_scene()

    def go_to_scene(self):
        Scene(self.game, self.new_scene, self.entry_point).enter_state()

    def create_scene(self):
        layers = []
        for layer in self.tmx_data.layers:
            layers.append(layer.name)

        if 'blocks' in layers:
            for x, y, surf in self.tmx_data.get_layer_by_name('blocks').tiles():
               Wall([self.block_sprites, self.drawn_sprites], (x * TILE_SIZE, y * TILE_SIZE), 'blocks', surf)

        if 'background' in layers:
            for x, y, surf in self.tmx_data.get_layer_by_name('background').tiles():
               Background([self.block_sprites, self.drawn_sprites], (x * TILE_SIZE, y * TILE_SIZE), 'background', surf)

        if 'semiblocks' in layers:
            for x, y, surf in self.tmx_data.get_layer_by_name('semiblocks').tiles():
                Barrier([self.block_sprites, self.drawn_sprites], (x * TILE_SIZE, y * TILE_SIZE), 'semiblocks', surf)

        if 'foreground' in layers:
            for x, y, surf in self.tmx_data.get_layer_by_name('foreground').tiles():
               Background([self.block_sprites, self.drawn_sprites], (x * TILE_SIZE, y * TILE_SIZE), 'foreground', surf)

        if 'entries' in layers:
            for obj in self.tmx_data.get_layer_by_name('entries'):
                if obj.name == f'{self.current_scene}':
                    self.player = Player(self.game, self, [self.update_sprites, self.drawn_sprites],
                                         (obj.x, obj.y),'blocks' , 'player')
                    self.target = self.player

        if 'entities' in layers:
            for obj in self.tmx_data.get_layer_by_name('entities'):
                if obj.name == 'enemy':
                    self.enemy = Enemy(self.game, self, [self.update_sprites, self.drawn_sprites],
                                         (obj.x, obj.y),'blocks' , 'enemy')
                if obj.name == 'chest':
                    self.chest = Chest(self.game, self, [self.update_sprites, self.drawn_sprites],
                                         (obj.x, obj.y),'characters' , 'chest')

        if 'exits' in layers:
            for obj in self.tmx_data.get_layer_by_name('exits'):
                Collider([self.exit_sprites], (obj.x, obj.y), (obj.width, obj.height), obj.name)


    def update(self, dt):
        self.update_sprites.update(dt)
        self.camera.update(dt, self.target)
        if self.player.check_chest_collision():
            EndScreen(self.game).enter_state()

    def debug(self, debug_list):
        for index, name in enumerate(debug_list):
            self.game.render_text(name, COLORS['white'], self.game.font, (8, 16 * index), False)

    def draw(self, screen):
        self.camera.draw(screen, self.drawn_sprites)
        if INPUTS['f12']:
            self.debug([
                str('FPS: ' +  str(round(self.game.clock.get_fps(), 2))),
                str('state: ' + str(self.player.state)),
            ])
