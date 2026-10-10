"""Определения предметов."""


class Item:
    def __init__(self, id, name, kind="resource", icon_color=(200, 200, 200),
                 stack=99, use_effect=None, description=""):
        self.id = id
        self.name = name
        self.kind = kind              # resource | tool | food | drink
        self.icon_color = icon_color
        self.stack = stack
        self.use_effect = use_effect  # fn(stats) для еды/питья
        self.description = description


def _berry(stats):
    stats.eat(12)
    stats.heal(2)


def _coconut(stats):
    stats.eat(18)
    stats.drink(20)


def _water(stats):
    stats.drink(30)


ITEMS = {
    "wood":    Item("wood", "Дерево", "resource", (140, 90, 40)),
    "stone":   Item("stone", "Камень", "resource", (150, 150, 150)),
    "fiber":   Item("fiber", "Волокно", "resource", (180, 210, 120)),
    "berry":   Item("berry", "Ягоды", "food", (220, 60, 90),
                    use_effect=_berry, description="Восстанавливает голод"),
    "coconut": Item("coconut", "Кокос", "food", (150, 100, 60),
                    use_effect=_coconut, description="Еда и вода"),
    "water":   Item("water", "Вода", "drink", (90, 170, 230),
                    use_effect=_water, description="Восстанавливает жажду"),
    "axe":     Item("axe", "Топор", "tool", (180, 180, 190), stack=1),
    "pickaxe": Item("pickaxe", "Кирка", "tool", (170, 170, 180), stack=1),
}