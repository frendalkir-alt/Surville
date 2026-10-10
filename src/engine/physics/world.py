"""Физический мир — список твёрдых прямоугольников."""
import pygame


class PhysicsWorld:
    def __init__(self, gravity=1800.0):
        self.gravity = gravity
        self.solids = []  # список pygame.Rect

    def add_solid(self, rect):
        self.solids.append(rect)

    def add_solids(self, rects):
        self.solids.extend(rects)

    def clear(self):
        self.solids.clear()

    def update_body(self, body, dt):
        body.gravity = self.gravity
        body.update(dt, self.solids)

    def query(self, rect):
        return [s for s in self.solids if s.colliderect(rect)]

    def draw_debug(self, surface, camera):
        for s in self.solids:
            pygame.draw.rect(surface, (90, 200, 120), s.move(camera.offset), 1)