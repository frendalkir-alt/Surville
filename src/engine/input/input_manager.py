"""Обёртка над вводом pygame: held / just_pressed / just_released."""
import pygame

_NUM_KEYS = 512


class InputManager:
    def __init__(self):
        self.keys = [False] * _NUM_KEYS
        self.prev_keys = [False] * _NUM_KEYS
        self.mouse_buttons = (False, False, False)
        self.prev_mouse = (False, False, False)
        self.mouse_pos = (0, 0)

    def update(self):
        pressed = pygame.key.get_pressed()
        self.prev_keys = self.keys
        self.keys = [bool(pressed[i]) for i in range(_NUM_KEYS)]

        self.prev_mouse = self.mouse_buttons
        self.mouse_buttons = pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()

    # --- клавиатура ---
    def key_held(self, key):
        return 0 <= key < _NUM_KEYS and self.keys[key]

    def key_pressed(self, key):
        return 0 <= key < _NUM_KEYS and self.keys[key] and not self.prev_keys[key]

    def key_released(self, key):
        return 0 <= key < _NUM_KEYS and not self.keys[key] and self.prev_keys[key]

    def axis(self, negative_key, positive_key):
        return (1 if self.key_held(positive_key) else 0) - \
               (1 if self.key_held(negative_key) else 0)

    # --- мышь ---
    def mouse_held(self, button=0):
        return 0 <= button < len(self.mouse_buttons) and self.mouse_buttons[button]

    def mouse_pressed(self, button=0):
        return (0 <= button < len(self.mouse_buttons)
                and self.mouse_buttons[button] and not self.prev_mouse[button])