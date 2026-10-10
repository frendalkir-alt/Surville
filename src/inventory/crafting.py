"""Рецепты крафта."""
from .items import ITEMS


RECIPES = {
    "axe":     {"wood": 3, "stone": 2, "fiber": 2},
    "pickaxe": {"wood": 2, "stone": 3, "fiber": 2},
}


def can_craft(inventory, item_id):
    if item_id not in RECIPES:
        return False
    return all(inventory.has(res, need) for res, need in RECIPES[item_id].items())


def craft(inventory, item_id):
    if not can_craft(inventory, item_id):
        return False
    for res, need in RECIPES[item_id].items():
        inventory.remove(res, need)
    inventory.add(item_id, 1)
    return True