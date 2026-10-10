"""Простые 2D-хелперы."""
import math


def clamp(value, low, high):
    return max(low, min(high, value))


def lerp(a, b, t):
    return a + (b - a) * t


def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def length(x, y):
    return math.hypot(x, y)


def normalize(x, y):
    l = length(x, y)
    if l == 0:
        return 0.0, 0.0
    return x / l, y / l