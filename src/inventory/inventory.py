"""Простой инвентарь: счётчик по id."""
from .items import ITEMS


class Inventory:
    def __init__(self):
        self.slots = {}  # id -> count

    def add(self, item_id, count=1):
        if item_id not in ITEMS:
            return
        self.slots[item_id] = self.slots.get(item_id, 0) + count

    def remove(self, item_id, count=1):
        if self.slots.get(item_id, 0) < count:
            return False
        self.slots[item_id] -= count
        if self.slots[item_id] <= 0:
            del self.slots[item_id]
        return True

    def count(self, item_id):
        return self.slots.get(item_id, 0)

    def has(self, item_id, count=1):
        return self.count(item_id) >= count

    def total_items(self):
        return sum(self.slots.values())

    def first_of_kind(self, kind, stats):
        """Возвращает id первого подходящего предмета и применяет его."""
        for item_id, n in self.slots.items():
            if n <= 0:
                continue
            it = ITEMS[item_id]
            if it.kind == kind and it.use_effect:
                return item_id
        return None

    def use(self, item_id, stats):
        if not self.has(item_id):
            return False
        it = ITEMS[item_id]
        if not it.use_effect:
            return False
        it.use_effect(stats)
        self.remove(item_id, 1)
        return True