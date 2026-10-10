import pygame

from ..engine.core.scene import Scene
from ..engine import config as cfg
from ..level import Level
from ..ui import HUD


class GameplayScene(Scene):
    def on_enter(self):
        self.level = Level(self.game)
        self.hud = HUD(self.game)

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        self.level.update(dt, self.game.input, mouse_pos)

        if not self.level.player.alive:
            self.game.last_score = self.level.score
            self.game.last_wave = self.level.spawner.wave
            self.game.scenes.switch("game_over")

    def draw(self, surface):
        surface.fill(cfg.BACKGROUND_COLOR)
        self.level.draw(surface)
        self.hud.draw(surface, self.level, int(self.game.clock.get_fps()))