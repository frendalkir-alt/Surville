"""Физическое тело с AABB-коллизиями против набора прямоугольников."""
import pygame


class Body:
    def __init__(self, x, y, width, height,
                 gravity=0.0, max_fall_speed=1200.0):
        self.position = pygame.Vector2(x, y)
        self.size = (width, height)
        self.velocity = pygame.Vector2(0, 0)
        self.gravity = gravity
        self.max_fall_speed = max_fall_speed

        self.on_ground = False
        self.collisions = {"left": False, "right": False,
                           "top": False, "bottom": False}

    @property
    def rect(self):
        return pygame.Rect(int(self.position.x), int(self.position.y), *self.size)

    def set_position(self, x, y):
        self.position.update(x, y)

    def apply_gravity(self, dt):
        if self.gravity:
            self.velocity.y += self.gravity * dt
            if self.velocity.y > self.max_fall_speed:
                self.velocity.y = self.max_fall_speed

    def update(self, dt, solids):
        self.apply_gravity(dt)
        self._move_x(dt, solids)
        self._move_y(dt, solids)

    def _move_x(self, dt, solids):
        self.collisions["left"] = False
        self.collisions["right"] = False

        self.position.x += self.velocity.x * dt
        rect = self.rect
        for s in solids:
            if rect.colliderect(s):
                if self.velocity.x > 0:
                    rect.right = s.left
                    self.collisions["right"] = True
                elif self.velocity.x < 0:
                    rect.left = s.right
                    self.collisions["left"] = True
                self.position.x = float(rect.x)
                self.velocity.x = 0

    def _move_y(self, dt, solids):
        self.collisions["top"] = False
        self.collisions["bottom"] = False
        self.on_ground = False

        self.position.y += self.velocity.y * dt
        rect = self.rect
        for s in solids:
            if rect.colliderect(s):
                if self.velocity.y > 0:
                    rect.bottom = s.top
                    self.collisions["bottom"] = True
                    self.on_ground = True
                elif self.velocity.y < 0:
                    rect.top = s.bottom
                    self.collisions["top"] = True
                self.position.y = float(rect.y)
                self.velocity.y = 0