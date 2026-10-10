"""Мир: остров, ресурсы, игрок, взаимодействие."""
import pygame

from .engine import config as cfg
from .player import Player
from .world import World


class Level:
    def __init__(self, game):
        self.game = game
        self.world = World(seed=cfg.WORLD_SEED)

        # игрок появляется в центре карты
        cx = self.world.terrain.pixel_width // 2
        cy = self.world.terrain.pixel_height // 2
        # чуть сдвинем, чтобы точно не в воде
        while not self.world.is_walkable(cx, cy):
            cy += 32
        self.player = Player(cx, cy)

    def update(self, dt, input_mgr):
        if not self.player.alive:
            return

        self.player.update(dt, input_mgr, self.world)

        # взаимодействие E
        if input_mgr.key_pressed(pygame.K_e):
            self._try_interact()

        # пить у воды: если рядом вода — можно пить по R
        if input_mgr.key_pressed(pygame.K_r):
            self._try_drink()

        # использовать предметы
        if input_mgr.key_pressed(pygame.K_f):
            self._eat_anything()

    def _try_interact(self):
        pos = self.player.body.rect.center
        res = self.world.nearest_resource(pos, cfg.INTERACT_RADIUS)
        if res is None:
            return
        drops = res.hit()
        if drops:
            for item_id, n in drops:
                self.player.inventory.add(item_id, n)

    def _try_drink(self):
        # если в радиусе 3 тайлов есть вода — пьём
        ts = cfg.TILE_SIZE
        cx, cy = self.player.body.rect.center
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                x = cx + dx * ts
                y = cy + dy * ts
                if not self.world.is_walkable(x, y):  # вода = неходибельно
                    self.player.stats.drink(25)
                    return

    def _eat_anything(self):
        inv = self.player.inventory
        for kind in ("food", "drink"):
            item_id = inv.first_of_kind(kind, self.player.stats)
            if item_id:
                inv.use(item_id, self.player.stats)
                return

    def draw(self, surface, camera):
        self.world.draw_terrain(surface, camera)
        self.world.draw_resources(surface, camera)

        # игрок
        ox, oy = camera.offset
        rect = self.player.body.rect.move(ox, oy)
        sprite_rect = self.player.sprite.get_rect(center=rect.center)
        if not (self.player.stats._invuln > 0 and
                int(self.player.stats._invuln * 20) % 2 == 0):
            surface.blit(self.player.sprite, sprite_rect)

        if cfg.DEBUG:
            pygame.draw.rect(surface, (255, 0, 0), rect, 1)

    def draw_interact_hint(self, surface, camera):
        """Подсказка если рядом ресурс."""
        pos = self.player.body.rect.center
        res = self.world.nearest_resource(pos, cfg.INTERACT_RADIUS)
        if res is None:
            return
        ox, oy = camera.offset
        x, y = res.pos.x + ox, res.pos.y + oy
        font = pygame.font.Font(None, 20)
        text = font.render(f"[E] {res.type.name}", True, (255, 255, 255))
        bg = pygame.Surface((text.get_width() + 8, text.get_height() + 4),
                            pygame.SRCALPHA)
        bg.fill((0, 0, 0, 160))
        surface.blit(bg, (x - bg.get_width() // 2, y - res.type.radius - 24))
        surface.blit(text, (x - text.get_width() // 2, y - res.type.radius - 22))