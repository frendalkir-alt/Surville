"""Игрок: top-down, survival."""
import pygame

from .engine.graphics.assets import assets
from .engine.physics.body import Body
from .engine import config as cfg
from .survival import SurvivalStats
from .inventory import Inventory


class Player:
    def __init__(self, x, y):
        r = cfg.PLAYER_RADIUS
        self.body = Body(x - r, y - r, r * 2, r * 2, gravity=0.0)
        self.stats = SurvivalStats()
        self.inventory = Inventory()
        self.facing = pygame.Vector2(1, 0)
        self.is_running = False

        size = r * 2 + 8
        self.sprite = assets.image("sprites/player/player.png", (size, size),
                                   fallback_color=(90, 180, 250))

    @property
    def alive(self):
        return not self.stats.dead

    def update(self, dt, input_mgr, world):
        # движение
        ax = input_mgr.axis(pygame.K_a, pygame.K_d)
        ay = input_mgr.axis(pygame.K_w, pygame.K_s)
        v = pygame.Vector2(ax, ay)
        wants_run = input_mgr.key_held(pygame.K_LSHIFT) or input_mgr.key_held(pygame.K_RSHIFT)
        self.is_running = wants_run and self.stats.can_sprint and v.length_squared() > 0

        if v.length_squared() > 0:
            v = v.normalize()
            speed = cfg.PLAYER_RUN_SPEED if self.is_running else cfg.PLAYER_WALK_SPEED
            self.body.velocity.x = v.x * speed
            self.body.velocity.y = v.y * speed
            self.facing = v
        else:
            self.body.velocity.x = 0
            self.body.velocity.y = 0

        # простая проверка "не в воде" по 4 углам
        self._move_with_water_check(dt, world)

        # статистика
        self.stats.update(dt, self.is_running)

    def _move_with_water_check(self, dt, world):
        r = self.body.rect
        next_x = self.body.position.x + self.body.velocity.x * dt
        next_y = self.body.position.y + self.body.velocity.y * dt

        # пробуем X
        test = pygame.Rect(int(next_x), int(r.y), r.width, r.height)
        if world.is_walkable(test.centerx, test.centery) and \
           world.is_walkable(test.left, test.top) and \
           world.is_walkable(test.right - 1, test.bottom - 1) and \
           world.is_walkable(test.left, test.bottom - 1) and \
           world.is_walkable(test.right - 1, test.top):
            self.body.position.x = next_x

        # пробуем Y
        test = pygame.Rect(int(self.body.position.x), int(next_y), r.width, r.height)
        if world.is_walkable(test.centerx, test.centery) and \
           world.is_walkable(test.left, test.top) and \
           world.is_walkable(test.right - 1, test.bottom - 1) and \
           world.is_walkable(test.left, test.bottom - 1) and \
           world.is_walkable(test.right - 1, test.top):
            self.body.position.y = next_y

    def draw(self, surface):
        r = self.sprite.get_rect(center=self.body.rect.center)
        if self.stats._invuln > 0 and int(self.stats._invuln * 20) % 2 == 0:
            return
        surface.blit(self.sprite, r)