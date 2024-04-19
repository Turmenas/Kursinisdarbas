import pygame
from config import *
from camera import Camera
from Characters import Player
from objects import Object, Wall
from pytmx.util_pygame import  load_pygame

class State:
    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def enter_state(self):
        if len(self.game.states) < 1:
            self.prev_state = self.game.states[-1]
        self.game.states.append(self)

    def exit_state(self):
        self.game.states.pop()

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

class TitleScreen(State):
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, dt):
        if INPUTS['space']:
            Scene(self.game).enter_state()
            self.game.reset_inputs()

    def draw(self, screen):
        screen.fill(COLORS['green'])
        self.game.render_text('This is the title screen, press space :)', COLORS['black'], self.game.font, (WIDTH/2, HEIGHT/2), centered=True)

class Scene(State):
    def __init__(self, game):
        State.__init__(self, game)

        self.camera = Camera(self)
        self.update_sprites = pygame.sprite.Group()
        self.drawn_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()

        self.tmx_data = load_pygame('scenes/0/0.tmx')
        self.create_scene()

    def create_scene(self):
        layers = []
        for layer in self.tmx_data.layers:
            layers.append(layer.name)

        if 'blocks' in layers:
            for x, y, surf in self.tmx_data.get_layer_by_name('blocks').tiles():
               Wall([self.block_sprites, self.drawn_sprites], (x * TILE_SIZE, y * TILE_SIZE), 'blocks', surf)

        if 'entries' in layers:
            for obj in self.tmx_data.get_layer_by_name('entries'):
                if obj.name == '0':
                    self.player = Player(self.game, self, [self.update_sprites, self.drawn_sprites],
                                         (obj.x, obj.y),'blocks' , 'player')


    def update(self, dt):
        self.update_sprites.update(dt)
        self.camera.update(dt, self.player)

    def debug(self, debug_list):
        for index, name in enumerate(debug_list):
            self.game.render_text(name, COLORS['white'], self.game.font, (8, 16 * index), False)

    def draw(self, screen):
        self.camera.draw(screen, self.drawn_sprites)
        if INPUTS['f12']:
            self.debug([
                str('FPS ' +  str(round(self.game.clock.get_fps(), 2))),
            ])