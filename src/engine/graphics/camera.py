"""2D-камера, следующая за целью."""
import pygame
from ..utils.math2d import clamp, lerp


class Camera:
    def __init__(self, width, height, world_width=None, world_height=None):
        self.view = pygame.Rect(0, 0, width, height)
        self.world_width = world_width
        self.world_height = world_height
        self.x = 0.0
        self.y = 0.0

    def set_world_bounds(self, width, height):
        self.world_width = width
        self.world_height = height
        self._clamp()

    def follow(self, target_rect, lerp_speed=6.0, dt=0.016):
        target_x = target_rect.centerx - self.view.width / 2
        target_y = target_rect.centery - self.view.height / 2
        t = clamp(lerp_speed * dt, 0.0, 1.0)
        self.x = lerp(self.x, target_x, t)
        self.y = lerp(self.y, target_y, t)
        self._clamp()

    def move_to(self, x, y):
        self.x = x
        self.y = y
        self._clamp()

    def _clamp(self):
        if self.world_width is not None:
            self.x = clamp(self.x, 0, max(0, self.world_width - self.view.width))
        else:
            self.x = max(0, self.x)
        if self.world_height is not None:
            self.y = clamp(self.y, 0, max(0, self.world_height - self.view.height))
        else:
            self.y = max(0, self.y)

    @property
    def offset(self):
        return (-int(self.x), -int(self.y))

    def world_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.view.width, self.view.height)

    def visible(self, rect):
        return self.world_rect().colliderect(rect)

    def to_screen(self, pos):
        ox, oy = self.offset
        return pos[0] + ox, pos[1] + oy