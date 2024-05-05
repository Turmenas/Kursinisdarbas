import pygame
from config import *
from Characters import NPC
from Enemy import Enemy

class Player(NPC):
    def __init__(self, game, scene, group, pos, z, name):
        super().__init__(game, scene, group, pos, z, name)
        self.state = Idle(self)
        self.alive = True

    def update(self, dt):
        self.get_direction()
        self.exit_scene()
        self.change_state()
        self.state.update_state(dt, self)


    def check_enemy_collision(self):
        enemies = pygame.sprite.Group()
        for sprite in self.scene.update_sprites:
            if isinstance(sprite, Enemy):
                enemies.add(sprite)

        if pygame.sprite.spritecollideany(self, enemies):
            return True

    def handle_death(self):
        if isinstance(self, Player):
            self.kill()
            self.game.running = False

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

    def exit_scene(self):
        for exit in self.scene.exit_sprites:
            if self.hitbox.colliderect(exit.rect):
                self.scene.new_scene = SCENE_DATA[int(self.scene.current_scene)][int(exit.number)]
                self.scene.entry_point = exit.number
                #self.scene.transition.exiting = True
                self.scene.go_to_scene()

class Idle:
    def __init__(self, player):
        player.frame_index=0

    def enter_state(self, player):
        if player.vel.magnitude() > 1:
            return Move(player)

        if INPUTS['right_click']:
            return Dodge(player)

        if INPUTS['left_click']:
            return Attack(player)

        if player.check_enemy_collision():
            return Death(player)

    def update_state(self, dt, player):
        player.animate(f'idle_{player.get_direction()}', 2 * dt)
        player.movement()
        player.physics(dt, player.frict)


class Move:
    def __init__(self, player):
        Idle.__init__(self, player)

    def enter_state(self, player):
        if player.vel.magnitude() < 1:
            return Idle(player)

        if INPUTS['right_click']:
            return Dodge(player)

        if INPUTS['left_click']:
            return Attack(player)

        if player.check_enemy_collision():
            return Death(player)

    def update_state(self, dt, player):
        player.animate(f'move_{player.get_direction()}', 3 * dt)
        player.movement()
        player.physics(dt, player.frict)


class Dodge:
    def __init__(self, player):
        Idle.__init__(self, player)
        INPUTS['right_click'] = False
        self.timer =1
        self.dodge_pending = False
        self.vel = player.vec_to_mouse(300)

    def enter_state(self, player):
        if INPUTS['right_click']:
            self.dodge_pending = True
        if self.timer <= 0:
            if self.dodge_pending:
                return Dodge(player)
            else:
                return Idle(player)

    def update_state(self, dt, player):
        self.timer -= dt
        player.animate(f'dodge', 10 * dt)
        player.physics(dt, -5)
        player.acc = vec()
        player.vel = self.vel

class Death:
    def __init__(self, player):
        Idle.__init__(self, player)

    def update_state(self, dt, player):
        player.handle_death()

class Attack:
    def __init__(self, player):
        Idle.__init__(self, player)
        INPUTS['left_click'] = False
        self.timer =1
        self.attack_pending = False
        self.vel = player.vec_to_mouse(20)
        self.attacking = True

    def enter_state(self, player):
        if INPUTS['right_click']:
            self.attack_pending = True
        if self.timer <= 0:
            if self.attack_pending:
                return Attack(player)
            else:
                self.attacking = False
                return Idle(player)

    def update_state(self, dt, player):
        self.timer -= dt
        player.animate(f'attack_right', 5 * dt)
        player.physics(dt, -5)
        player.acc = vec()
        player.vel = self.vel