"""Биомы острова."""
from ..engine import config as cfg


class BiomeKind:
    WATER = "water"
    BEACH = "beach"
    GRASS = "grass"
    JUNGLE = "jungle"
    ROCK = "rock"


# Чем дальше от центра — тем ближе к воде
DISTANCE_ORDER = [
    (1.00, BiomeKind.WATER),
    (0.86, BiomeKind.BEACH),
    (0.60, BiomeKind.GRASS),
    (0.34, BiomeKind.JUNGLE),
    (0.00, BiomeKind.ROCK),
]


class Biome:
    def __init__(self, kind):
        self.kind = kind
        self.color = cfg.BIOME_COLORS.get(kind, (255, 0, 255))

    @property
    def is_walkable(self):
        return self.kind != BiomeKind.WATER

    @property
    def is_water(self):
        return self.kind == BiomeKind.WATER