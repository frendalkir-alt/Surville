"""Ресурсы: деревья, кусты, камни, кокосы."""
import pygame

from ..engine import config as cfg
from .biomes import BiomeKind


class Resource:
    """Описание типа ресурса."""
    def __init__(self, id, name, biomes, hp, drop, color, radius=18, regrow=0.0):
        self.id = id
        self.name = name
        self.biomes = set(biomes)     # в каких биомах может стоять
        self.hp = hp                  # сколько ударов
        self.drop = drop              # список (item_id, count)
        self.color = color
        self.radius = radius
        self.regrow = regrow          # сек до восстановления, 0 = вечно сломан


RESOURCE_TYPES = {
    "tree":   Resource("tree", "Дерево", [BiomeKind.GRASS, BiomeKind.JUNGLE],
                       hp=3, drop=[("wood", 2), ("fiber", 1)],
                       color=(70, 110, 50), radius=20),
    "bush":   Resource("bush", "Куст", [BiomeKind.GRASS, BiomeKind.JUNGLE],
                       hp=1, drop=[("berry", 2), ("fiber", 1)],
                       color=(80, 150, 70), radius=14),
    "rock":   Resource("rock", "Валун", [BiomeKind.ROCK, BiomeKind.GRASS],
                       hp=4, drop=[("stone", 3)],
                       color=(120, 120, 130), radius=18),
    "palm":   Resource("palm", "Пальма", [BiomeKind.BEACH],
                       hp=2, drop=[("wood", 2), ("coconut", 1)],
                       color=(110, 130, 70), radius=18),
}


class ResourceNode:
    """Конкретный экземпляр на карте."""
    def __init__(self, type_id, x, y):
        self.type_id = type_id
        self.type = RESOURCE_TYPES[type_id]
        self.pos = pygame.Vector2(x, y)
        self.hp = self.type.hp
        self.depleted = False

    @property
    def rect(self):
        r = self.type.radius
        return pygame.Rect(int(self.pos.x - r), int(self.pos.y - r), r * 2, r * 2)

    def hit(self):
        """Возвращает список (item_id, count) при разрушении, иначе None."""
        if self.depleted:
            return None
        self.hp -= 1
        if self.hp <= 0:
            self.depleted = True
            return list(self.type.drop)
        return None

    def draw(self, surface):
        if self.depleted:
            # пенёк/обломок
            c = (self.type.color[0] // 2, self.type.color[1] // 2, self.type.color[2] // 2)
            pygame.draw.circle(surface, c, (int(self.pos.x), int(self.pos.y)),
                               self.type.radius // 2)
            return
        pygame.draw.circle(surface, self.type.color,
                           (int(self.pos.x), int(self.pos.y)), self.type.radius)
        pygame.draw.circle(surface, (0, 0, 0),
                           (int(self.pos.x), int(self.pos.y)), self.type.radius, 2)