"""HUD: HP, голод, жажда, стамина, инвентарь, часы, подсказки."""
import pygame

from .engine import config as cfg
from .inventory import ITEMS


class HUD:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 22)
        self.small = pygame.font.Font(None, 18)
        self.big = pygame.font.Font(None, 42)

    def draw(self, surface, level, daynight, fps):
        p = level.player
        self._bar(surface, 20, 20, 240, 18, p.stats.hp / cfg.PLAYER_MAX_HP,
                  (200, 60, 60), f"HP {int(p.stats.hp)}")
        self._bar(surface, 20, 44, 240, 14, p.stats.hunger / cfg.PLAYER_MAX_HUNGER,
                  (210, 150, 60), f"Еда {int(p.stats.hunger)}", small=True)
        self._bar(surface, 20, 62, 240, 14, p.stats.thirst / cfg.PLAYER_MAX_THIRST,
                  (80, 160, 220), f"Вода {int(p.stats.thirst)}", small=True)
        self._bar(surface, 20, 80, 240, 12, p.stats.stamina / cfg.PLAYER_MAX_STAMINA,
                  (180, 200, 90), f"Сила {int(p.stats.stamina)}", small=True)

        self._inventory(surface, p.inventory)
        self._clock(surface, daynight)
        self._hint(surface)
        self._fps(surface, fps)

    def _bar(self, surface, x, y, w, h, ratio, color, label, small=False):
        pygame.draw.rect(surface, (30, 30, 40), (x, y, w, h))
        pygame.draw.rect(surface, color, (x, y, int(w * max(0.0, ratio)), h))
        pygame.draw.rect(surface, (230, 230, 230), (x, y, w, h), 1)
        font = self.small if small else self.font
        text = font.render(label, True, (255, 255, 255))
        surface.blit(text, (x + w + 10, y + max(0, (h - text.get_height()) // 2)))

    def _inventory(self, surface, inv):
        x, y = 20, cfg.WINDOW_HEIGHT - 140
        title = self.font.render("Инвентарь", True, (230, 230, 230))
        surface.blit(title, (x, y))
        y += 26
        if not inv.slots:
            t = self.small.render("(пусто)", True, (150, 150, 150))
            surface.blit(t, (x, y))
            return
        for item_id, count in sorted(inv.slots.items()):
            item = ITEMS.get(item_id)
            if not item:
                continue
            pygame.draw.rect(surface, item.icon_color, (x, y + 2, 14, 14))
            pygame.draw.rect(surface, (0, 0, 0), (x, y + 2, 14, 14), 1)
            text = self.small.render(f"{item.name} × {count}", True, (220, 220, 220))
            surface.blit(text, (x + 22, y))
            y += 18

    def _clock(self, surface, daynight):
        x = cfg.WINDOW_WIDTH - 140
        text = self.font.render(daynight.clock_str(), True, (240, 240, 240))
        surface.blit(text, (x, 16))
        phase = "Ночь" if daynight.is_night else "День"
        pcolor = (150, 150, 200) if daynight.is_night else (240, 220, 140)
        pt = self.small.render(phase, True, pcolor)
        surface.blit(pt, (x, 40))

    def _hint(self, surface):
        controls = "WASD — ходьба,  Shift — бег,  E — действие,  F — съесть,  R — попить"
        text = self.small.render(controls, True, (170, 170, 170))
        surface.blit(text, (20, cfg.WINDOW_HEIGHT - 22))

    def _fps(self, surface, fps):
        text = self.small.render(f"FPS {fps}", True, (120, 120, 120))
        surface.blit(text, (cfg.WINDOW_WIDTH - text.get_width() - 10, cfg.WINDOW_HEIGHT - 20))