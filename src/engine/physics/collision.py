"""Утилиты для AABB-коллизий."""
import pygame


def aabb_overlap(a: pygame.Rect, b: pygame.Rect) -> bool:
    return a.colliderect(b)


def point_in_rect(point, rect: pygame.Rect) -> bool:
    return rect.collidepoint(point)


def rect_vs_rects(rect: pygame.Rect, rects):
    return [r for r in rects if rect.colliderect(r)]


def tile_at(world_x, world_y, tile_size):
    """Возвращает (tile_x, tile_y) по мировым координатам."""
    return int(world_x // tile_size), int(world_y // tile_size)