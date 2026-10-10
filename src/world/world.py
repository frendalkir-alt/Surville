"""Собирает террейн и ресурсы в один объект."""
import math
import random
import pygame

from ..engine import config as cfg
from .biomes import Biome, BiomeKind
from .terrain import IslandTerrain
from .resources import RESOURCE_TYPES, ResourceNode


class World:
    def __init__(self, seed=None):
        self.terrain = IslandTerrain(seed=seed)
        self.rng = random.Random(seed if seed is not None else cfg.WORLD_SEED)

        # кэш биомов
        self._biomes = {k: Biome(k) for k in cfg.BIOME_COLORS.keys()}

        self.resources = self._scatter_resources()

    def biome_color(self, tx, ty):
        return self._biomes[self.terrain.biome_at(tx, ty)].color

    def _scatter_resources(self):
        resources = []
        ts = self.terrain.tile_size
        for ty in range(self.terrain.h):
            for tx in range(self.terrain.w):
                biome = self.terrain.biome_at(tx, ty)
                for rid, rtype in RESOURCE_TYPES.items():
                    if biome not in rtype.biomes:
                        continue
                    # вероятность появления
                    density = {
                        BiomeKind.BEACH: 0.02,
                        BiomeKind.GRASS: 0.05,
                        BiomeKind.JUNGLE: 0.12,
                        BiomeKind.ROCK: 0.08,
                    }.get(biome, 0.0)
                    if self.rng.random() < density:
                        x = tx * ts + ts / 2 + self.rng.uniform(-12, 12)
                        y = ty * ts + ts / 2 + self.rng.uniform(-12, 12)
                        resources.append(ResourceNode(rid, x, y))
                        break  # максимум один ресурс на тайл
        return resources

    # --- API для сцены ---

    def nearest_resource(self, pos, radius):
        best, best_d = None, radius * radius
        for r in self.resources:
            if r.depleted:
                continue
            dx = r.pos.x - pos[0]
            dy = r.pos.y - pos[1]
            d = dx * dx + dy * dy
            if d < best_d:
                best_d = d
                best = r
        return best

    def is_walkable(self, x, y):
        return self.terrain.is_walkable_px(x, y)

    def draw_terrain(self, surface, camera):
        ts = self.terrain.tile_size
        view = camera.world_rect()

        tx0 = max(0, view.left // ts)
        ty0 = max(0, view.top // ts)
        tx1 = min(self.terrain.w, view.right // ts + 2)
        ty1 = min(self.terrain.h, view.bottom // ts + 2)

        ox, oy = camera.offset
        for ty in range(ty0, ty1):
            for tx in range(tx0, tx1):
                color = self.biome_color(tx, ty)
                rect = pygame.Rect(tx * ts + ox, ty * ts + oy, ts + 1, ts + 1)
                pygame.draw.rect(surface, color, rect)

    def draw_resources(self, surface, camera):
        view = camera.world_rect()
        ox, oy = camera.offset
        for r in self.resources:
            if not view.colliderect(r.rect):
                continue
            screen_pos = (r.pos.x + ox, r.pos.y + oy)
            if r.depleted:
                c = (r.type.color[0] // 2, r.type.color[1] // 2, r.type.color[2] // 2)
                pygame.draw.circle(surface, c, screen_pos, r.type.radius // 2)
                continue
            pygame.draw.circle(surface, r.type.color, screen_pos, r.type.radius)
            pygame.draw.circle(surface, (0, 0, 0), screen_pos, r.type.radius, 2)