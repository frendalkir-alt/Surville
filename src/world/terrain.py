"""Генерация острова."""
import math
import random

from ..engine import config as cfg
from .biomes import BiomeKind, DISTANCE_ORDER


class IslandTerrain:
    def __init__(self, width_tiles=None, height_tiles=None, seed=None):
        self.w = width_tiles or cfg.WORLD_TILES_X
        self.h = height_tiles or cfg.WORLD_TILES_Y
        self.seed = seed if seed is not None else cfg.WORLD_SEED
        self.tile_size = cfg.TILE_SIZE
        self.biome_grid = self._generate()

    def _generate(self):
        rng = random.Random(self.seed)
        cx, cy = self.w / 2.0, self.h / 2.0
        max_r = min(cx, cy)
        grid = []
        for y in range(self.h):
            row = []
            for x in range(self.w):
                # небольшое искажение краёв
                wobble = (math.sin(x * 0.35 + self.seed) +
                          math.cos(y * 0.31 - self.seed)) * 0.04
                d = math.hypot(x - cx, y - cy) / max_r + wobble
                biome = BiomeKind.ROCK
                for threshold, kind in DISTANCE_ORDER:
                    if d > threshold:
                        biome = kind
                        break
                row.append(biome)
            grid.append(row)
        return grid

    def biome_at(self, tx, ty):
        if 0 <= ty < self.h and 0 <= tx < len(self.biome_grid[ty]):
            return self.biome_grid[ty][tx]
        return BiomeKind.WATER

    def biome_at_px(self, x, y):
        return self.biome_at(int(x // self.tile_size), int(y // self.tile_size))

    def is_walkable_px(self, x, y):
        return self.biome_at_px(x, y) != BiomeKind.WATER

    @property
    def pixel_width(self):
        return self.w * self.tile_size

    @property
    def pixel_height(self):
        return self.h * self.tile_size