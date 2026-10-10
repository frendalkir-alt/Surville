import pygame

from ..engine.core.scene import Scene
from ..engine import config as cfg


class MenuScene(Scene):
    def on_enter(self):
        self.font_big = pygame.font.Font(None, 96)
        self.font_mid = pygame.font.Font(None, 28)
        self.blink = 0.0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
            self.game.scenes.switch("gameplay")

    def update(self, dt):
        self.blink += dt

    def draw(self, surface):
        surface.fill(cfg.BACKGROUND_COLOR)
        title = self.font_big.render("SURVILLE", True, (240, 200, 90))
        surface.blit(title, title.get_rect(center=(self.game.width // 2, 200)))
        sub = self.font_mid.render("Выживи как можно дольше", True, (200, 200, 200))
        surface.blit(sub, sub.get_rect(center=(self.game.width // 2, 290)))
        if int(self.blink * 2) % 2 == 0:
            hint = self.font_mid.render("Нажми SPACE", True, (255, 255, 255))
            surface.blit(hint, hint.get_rect(center=(self.game.width // 2, 420)))
        ctrl = self.font_mid.render("WASD — движение,  ЛКМ — стрелять",
                                    True, (170, 170, 170))
        surface.blit(ctrl, ctrl.get_rect(center=(self.game.width // 2, 500)))