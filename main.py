import pygame, sys, os
from states import TitleScreen
from config import *


class Game:
    def __init__(self):

        pygame.init()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN|pygame.SCALED)
        self.font = pygame.font.Font(FONT, TILE_SIZE)
        self.running = True
        self.image = pygame.Surface((100,100))
        self.rect = self.image.get_frect()

        self.states = []
        self.title_screen = TitleScreen(self)
        self.states.append(self.title_screen)

    def render_text(self, text, color, font, pos, centered=True):
        surf = font.render(str(text), False, color)
        rect = surf.get_rect(center = pos) if centered else surf.get_rect(topleft = pos)
        self.screen.blit(surf, rect)

    def cursor(self, screen):
        pygame.mouse.set_visible(False)
        cursor_img = pygame.image.load('assets/crosshair.png').convert_alpha()
        cursor_rect = cursor_img.get_rect(center = pygame.mouse.get_pos())
        screen.blit(cursor_img, cursor_rect)

    def get_images(self, path):
        images = []
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            img = pygame.image.load(full_path).convert_alpha()
            images.append(img)
        return images

    def get_animations(self, path):
        animations = {}
        for file_name in os.listdir(path):
            animations.update({file_name:[]})
        return animations

    def get_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    INPUTS['escape'] = True
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    INPUTS['space'] = True
                elif event.key == pygame.K_a:
                    INPUTS['a'] = True
                elif event.key == pygame.K_d:
                    INPUTS['d'] = True
                elif event.key == pygame.K_w:
                    INPUTS['w'] = True
                elif event.key == pygame.K_s:
                    INPUTS['s'] = True
                elif event.key == pygame.K_F12:
                    INPUTS['f12'] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    INPUTS['space'] = False
                elif event.key == pygame.K_a:
                    INPUTS['a'] = False
                elif event.key == pygame.K_d:
                    INPUTS['d'] = False
                elif event.key == pygame.K_w:
                    INPUTS['w'] = False
                elif event.key == pygame.K_s:
                    INPUTS['s'] = False
                elif event.key == pygame.K_F12:
                    INPUTS['f12'] = False

            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                   INPUTS['scroll_up'] = True
                elif event.y == -1:
                   INPUTS['scroll_down'] = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                   INPUTS['left_click'] = True
                elif event.button == 3:
                   INPUTS['right_click'] = True
                elif event.button == 4:
                   INPUTS['scroll_down'] = True
                elif event.button == 2:
                   INPUTS['scroll_up'] = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                   INPUTS['left_click'] = False
                elif event.button == 3:
                   INPUTS['right_click'] = False
                elif event.button == 4:
                   INPUTS['scroll_down'] = False
                elif event.button == 2:
                   INPUTS['scroll_up'] = False

    def reset_inputs(self):
        for key in INPUTS:
            INPUTS[key] = False

    def loop(self):
        while self.running:
            dt = self.clock.tick(self.fps)/1000
            self.get_inputs()
            self.states[-1].update(dt)
            self.states[-1].draw(self.screen)
            self.cursor(self.screen)
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.loop()