"""Surville — точка входа."""
import pygame

from src.engine.core.game import Game
from src.engine.core.scene import Scene
from src.engine.graphics.camera import Camera
from src.engine import config as cfg
from src.level import Level
from src.ui import HUD
from src.daynight import DayNightCycle
from src.craft_menu import CraftMenu

class GameplayScene(Scene):
    def on_enter(self):
        self.level = Level(self.game)
        self.camera = Camera(
            cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT,
            self.level.world.terrain.pixel_width,
            self.level.world.terrain.pixel_height,
        )
        # поставим камеру на игрока сразу
        self.camera.move_to(
            self.level.player.body.rect.centerx - cfg.WINDOW_WIDTH // 2,
            self.level.player.body.rect.centery - cfg.WINDOW_HEIGHT // 2,
        )
        self.hud = HUD(self.game)
        self.daynight = DayNightCycle()
        self.craft_menu = CraftMenu(self.game)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            self.craft_menu.toggle()
            return
        self.craft_menu.handle_event(event)

    def update(self, dt):
        self.craft_menu.update(dt)

        # мир на паузе пока открыто меню
        if self.craft_menu.open:
            return

        self.level.update(dt, self.game.input)
        self.daynight.update(dt)

        target = self.level.player.body.rect
        cam = self.camera
        tx = target.centerx - cam.view.width / 2
        ty = target.centery - cam.view.height / 2
        cam.x += (tx - cam.x) * min(1.0, dt * 6)
        cam.y += (ty - cam.y) * min(1.0, dt * 6)
        cam._clamp()

        if not self.level.player.alive:
            self.game.last_time = self.daynight.clock_str()
            self.game.scenes.switch("game_over")

    def draw(self, surface):
        surface.fill(cfg.BACKGROUND_COLOR)
        self.level.draw(surface, self.camera)
        self.daynight.draw(surface)
        self.level.draw_interact_hint(surface, self.camera)
        self.hud.draw(surface, self.level, self.daynight, int(self.game.clock.get_fps()))
        self.craft_menu.draw(surface, self.level.player.inventory)


class GameOverScene(Scene):
    def on_enter(self):
        self.big = pygame.font.Font(None, 96)
        self.mid = pygame.font.Font(None, 30)
        self.blink = 0.0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game.scenes.switch("gameplay")

    def update(self, dt):
        self.blink += dt

    def draw(self, surface):
        surface.fill((20, 12, 12))
        t1 = self.big.render("Ты не выжил", True, (220, 80, 80))
        surface.blit(t1, t1.get_rect(center=(cfg.WINDOW_WIDTH // 2, 260)))
        t2 = self.mid.render(f"Время: {getattr(self.game, 'last_time', '??:??')}",
                             True, (230, 230, 230))
        surface.blit(t2, t2.get_rect(center=(cfg.WINDOW_WIDTH // 2, 360)))
        if int(self.blink * 2) % 2 == 0:
            t3 = self.mid.render("SPACE — снова", True, (255, 255, 255))
            surface.blit(t3, t3.get_rect(center=(cfg.WINDOW_WIDTH // 2, 440)))


class MenuScene(Scene):
    def on_enter(self):
        self.big = pygame.font.Font(None, 96)
        self.mid = pygame.font.Font(None, 28)
        self.blink = 0.0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
            self.game.scenes.switch("gameplay")

    def update(self, dt):
        self.blink += dt

    def draw(self, surface):
        surface.fill(cfg.BACKGROUND_COLOR)
        t = self.big.render("SURVILLE", True, (240, 200, 90))
        surface.blit(t, t.get_rect(center=(cfg.WINDOW_WIDTH // 2, 200)))
        s = self.mid.render("Ты выжил после крушения. Продержись как можно дольше.",
                            True, (200, 200, 200))
        surface.blit(s, s.get_rect(center=(cfg.WINDOW_WIDTH // 2, 290)))
        if int(self.blink * 2) % 2 == 0:
            h = self.mid.render("SPACE — начать", True, (255, 255, 255))
            surface.blit(h, h.get_rect(center=(cfg.WINDOW_WIDTH // 2, 400)))


def main():
    game = Game()
    game.last_time = "??:??"
    game.scenes.register("menu", MenuScene(game))
    game.scenes.register("gameplay", GameplayScene(game))
    game.scenes.register("game_over", GameOverScene(game))
    game.run("menu")


if __name__ == "__main__":
    main()