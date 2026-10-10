"""Меню крафта. Открывается на C, навигация стрелками, крафт на Enter."""
import pygame

from .engine import config as cfg
from .inventory import ITEMS, RECIPES, can_craft, craft


class CraftMenu:
    PANEL_W = 460
    PANEL_H = 420
    LINE_H = 34

    def __init__(self, game):
        self.game = game
        self.open = False
        self.selected = 0
        self.feedback = ""             # сообщение об успехе/ошибке
        self.feedback_timer = 0.0
        self.recipe_ids = list(RECIPES.keys())

        self.font_big = pygame.font.Font(None, 34)
        self.font = pygame.font.Font(None, 22)
        self.small = pygame.font.Font(None, 18)

    # --- API ---

    def toggle(self):
        self.open = not self.open
        self.feedback = ""
        self.feedback_timer = 0.0

    def handle_event(self, event):
        if not self.open:
            return
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_c or event.key == pygame.K_ESCAPE:
            self.open = False
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.selected = (self.selected - 1) % len(self.recipe_ids)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.selected = (self.selected + 1) % len(self.recipe_ids)
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_e):
            self._craft_selected()

    def update(self, dt):
        if self.feedback_timer > 0:
            self.feedback_timer = max(0.0, self.feedback_timer - dt)

    # --- internal ---

    def _craft_selected(self):
        if not self.recipe_ids:
            return
        item_id = self.recipe_ids[self.selected]
        player = self.game.scenes.current.level.player

        if craft(player.inventory, item_id):
            self.feedback = f"Создано: {ITEMS[item_id].name}"
        else:
            self.feedback = "Не хватает ресурсов"
        self.feedback_timer = 1.6

    # --- render ---

    def draw(self, surface, inventory):
        if not self.open:
            return

        # затемнение
        overlay = pygame.Surface((cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT),
                                 pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        px = (cfg.WINDOW_WIDTH - self.PANEL_W) // 2
        py = (cfg.WINDOW_HEIGHT - self.PANEL_H) // 2

        panel = pygame.Rect(px, py, self.PANEL_W, self.PANEL_H)
        pygame.draw.rect(surface, (32, 34, 44), panel, border_radius=10)
        pygame.draw.rect(surface, (110, 120, 150), panel, 2, border_radius=10)

        title = self.font_big.render("Крафт", True, (240, 220, 140))
        surface.blit(title, (px + 20, py + 14))

        hint = self.small.render("↑↓ — выбор,  Enter — создать,  C/Esc — закрыть",
                                 True, (170, 170, 180))
        surface.blit(hint, (px + 20, py + 50))

        y = py + 84
        for i, item_id in enumerate(self.recipe_ids):
            self._draw_recipe_row(surface, px, y, item_id, i, inventory)
            y += self.LINE_H + 22

        if self.feedback and self.feedback_timer > 0:
            color = (140, 230, 140) if "Создано" in self.feedback else (230, 140, 140)
            text = self.font.render(self.feedback, True, color)
            surface.blit(text, (px + 20, py + self.PANEL_H - 34))

    def _draw_recipe_row(self, surface, px, y, item_id, index, inventory):
        item = ITEMS[item_id]
        selected = (index == self.selected)
        craftable = can_craft(inventory, item_id)

        row_rect = pygame.Rect(px + 12, y - 4, self.PANEL_W - 24, self.LINE_H + 18)
        if selected:
            pygame.draw.rect(surface, (58, 62, 84), row_rect, border_radius=6)
            pygame.draw.rect(surface, (200, 200, 220), row_rect, 1, border_radius=6)

        # иконка
        icon_rect = pygame.Rect(px + 22, y + 4, 24, 24)
        pygame.draw.rect(surface, item.icon_color, icon_rect, border_radius=4)
        pygame.draw.rect(surface, (0, 0, 0), icon_rect, 1, border_radius=4)

        # название
        name_color = (240, 240, 240) if craftable else (150, 150, 150)
        name = self.font.render(item.name, True, name_color)
        surface.blit(name, (px + 56, y + 6))

        # ингредиенты
        parts = []
        for res_id, need in RECIPES[item_id].items():
            have = inventory.count(res_id)
            parts.append((res_id, need, have))
        x = px + 56
        for res_id, need, have in parts:
            res = ITEMS[res_id]
            ok = have >= need
            text = f"{res.name} {have}/{need}"
            color = (140, 220, 140) if ok else (220, 130, 130)
            t = self.small.render(text, True, color)
            surface.blit(t, (x, y + 30))
            x += t.get_width() + 14