"""Главный игровой цикл."""
import sys
import pygame

from .. import config
from ..audio.sound import audio
from ..graphics.assets import assets
from ..input.input_manager import InputManager
from .scene import SceneManager


class Game:
    def __init__(self, title=None, width=None, height=None, fps=None):
        self.title = title or config.WINDOW_TITLE
        self.width = width or config.WINDOW_WIDTH
        self.height = height or config.WINDOW_HEIGHT
        self.fps = fps or config.FPS

        pygame.init()
        audio.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        self.clock = pygame.time.Clock()
        self.running = False

        self.input = InputManager()
        self.scenes = SceneManager(self)
        self.assets = assets

    def run(self, start_scene):
        self.scenes.switch(start_scene)
        self.running = True

        while self.running:
            raw_dt = self.clock.tick(self.fps) / 1000.0
            dt = min(raw_dt, 0.05)  # защита от «прыжков» после лагов

            self._handle_events()
            self.input.update()
            self.scenes.update(dt)

            self.screen.fill(config.BACKGROUND_COLOR)
            self.scenes.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit(0)

    def quit(self):
        self.running = False

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            self.scenes.handle_event(event)