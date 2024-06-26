from pygame import Vector2 as vec

HEIGHT = 224
WIDTH = 400
TILE_SIZE = 16
FONT = 'assets/pixelartfont.ttf'

INPUTS = {'escape': False, 'space': False, 'w': False, 's': False, 'd': False, 'a': False, 'left_click': False,
          'right_click': False, 'sroll_up': False, 'sroll_down': False, 'f12': False, 'e': False}

COLORS = {'black': (0, 0, 0), 'white': (255, 255, 255), 'red': (200, 100, 100), 'green': (100, 200, 100), 'blue': (100, 100, 200), 'kindablack': (28,17,23)}

LAYERS = ['background', 'objects', 'characters', 'semiblocks', 'blocks', 'foreground']

SCENE_DATA = {
    0:{1:1},
    1:{2:2}
}