"""Голод, жажда, стамина."""
from ..engine import config as cfg


class SurvivalStats:
    def __init__(self):
        self.hp = cfg.PLAYER_MAX_HP
        self.hunger = cfg.PLAYER_MAX_HUNGER
        self.thirst = cfg.PLAYER_MAX_THIRST
        self.stamina = cfg.PLAYER_MAX_STAMINA
        self.dead = False
        self._invuln = 0.0

    def update(self, dt, is_running):
        if self.dead:
            return
        self._invuln = max(0.0, self._invuln - dt)

        self.hunger = max(0.0, self.hunger - cfg.HUNGER_DECAY * dt)
        self.thirst = max(0.0, self.thirst - cfg.THIRST_DECAY * dt)

        if self.hunger <= 0 or self.thirst <= 0:
            self._apply_damage(cfg.STARVING_DAMAGE * dt)

        if is_running and self.stamina > 0:
            self.stamina = max(0.0, self.stamina - cfg.STAMINA_DRAIN * dt)
        else:
            self.stamina = min(cfg.PLAYER_MAX_STAMINA,
                               self.stamina + cfg.STAMINA_REGEN * dt)

    def _apply_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0.0
            self.dead = True

    def damage(self, amount):
        if self.dead or self._invuln > 0:
            return False
        self.hp -= amount
        self._invuln = cfg.PLAYER_INVULN_ON_HIT
        if self.hp <= 0:
            self.hp = 0.0
            self.dead = True
        return True

    def eat(self, amount):
        self.hunger = min(cfg.PLAYER_MAX_HUNGER, self.hunger + amount)

    def drink(self, amount):
        self.thirst = min(cfg.PLAYER_MAX_THIRST, self.thirst + amount)

    def heal(self, amount):
        self.hp = min(cfg.PLAYER_MAX_HP, self.hp + amount)

    @property
    def can_sprint(self):
        return self.stamina > 5.0