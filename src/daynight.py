"""Цикл дня и ночи — просто tint-оверлей."""
import pygame

from .engine import config as cfg


class DayNightCycle:
    def __init__(self):
        self.time = 0.0
        self.duration = cfg.DAY_DURATION
        self.overlay = pygame.Surface((cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT),
                                      pygame.SRCALPHA)

    def update(self, dt):
        self.time = (self.time + dt) % self.duration

    @property
    def phase(self):
        """0..1 — доля суток."""
        return self.time / self.duration

    @property
    def is_night(self):
        return self.phase >= cfg.NIGHT_START

    def alpha(self):
        p = self.phase
        if p < cfg.NIGHT_START:
            # плавное затемнение к ночи
            t = p / cfg.NIGHT_START
            return int(cfg.NIGHT_MAX_ALPHA * max(0.0, (t - 0.7) / 0.3))
        # ночь
        return cfg.NIGHT_MAX_ALPHA

    def draw(self, surface):
        a = self.alpha()
        if a <= 0:
            return
        self.overlay.fill((*cfg.NIGHT_COLOR, a))
        surface.blit(self.overlay, (0, 0))

    def clock_str(self):
        """HH:MM."""
        p = self.phase
        total_min = int(p * 24 * 60)
        h = (total_min // 60 + 6) % 24  # день начинается в 6:00
        m = total_min % 60
        return f"{h:02d}:{m:02d}"