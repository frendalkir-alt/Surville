import pygame

from ..engine.core.scene import Scene


class GameOverScene(Scene):
    def on_enter(self):
        self.font_big = pygame.font.Font(None, 96)
        self.font_mid = pygame.font.Font(None, 30)
        self.blink = 0.0
        self.score = getattr(self.game, "last_score", 0)
        self.wave = getattr(self.game, "last_wave", 0)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_SPACE:
            self.game.scenes.switch("gameplay")
        elif event.key == pygame.K_ESCAPE:
            self.game.scenes.switch("menu")

    def update(self, dt):
        self.blink += dt

    def draw(self, surface):
        surface.fill((30, 15, 20))
        t1 = self.font_big.render("Ты погиб", True, (230, 90, 90))
        surface.blit(t1, t1.get_rect(center=(self.game.width // 2, 200)))
        t2 = self.font_mid.render(f"Очки: {self.score}", True, (235, 235, 235))
        surface.blit(t2, t2.get_rect(center=(self.game.width // 2, 300)))
        t3 = self.font_mid.render(f"Волн пройдено: {self.wave}", True, (235, 235, 235))
        surface.blit(t3, t3.get_rect(center=(self.game.width // 2, 340)))
        if int(self.blink * 2) % 2 == 0:
            hint = self.font_mid.render("SPACE — заново,  ESC — меню",
                                        True, (255, 255, 255))
            surface.blit(hint, hint.get_rect(center=(self.game.width // 2, 470)))