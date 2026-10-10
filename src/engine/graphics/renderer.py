"""Обёртка над pygame.draw и blit — учитывает камеру."""
import pygame


class Renderer:
    def __init__(self, screen, camera=None):
        self.screen = screen
        self.camera = camera
        self._default_font = pygame.font.Font(None, 24)

    def set_camera(self, camera):
        self.camera = camera

    def blit(self, surface, pos, anchor="topleft", screen_space=False):
        rect = surface.get_rect(**{anchor: pos})
        if self.camera and not screen_space:
            rect = rect.move(self.camera.offset)
        self.screen.blit(surface, rect)
        return rect

    def draw_rect(self, color, rect, width=0, screen_space=False):
        if self.camera and not screen_space:
            rect = rect.move(self.camera.offset)
        pygame.draw.rect(self.screen, color, rect, width)

    def draw_text(self, text, pos, color=(255, 255, 255), font=None,
                  anchor="topleft", screen_space=True):
        font = font or self._default_font
        surf = font.render(text, True, color)
        rect = surf.get_rect(**{anchor: pos})
        if self.camera and not screen_space:
            rect = rect.move(self.camera.offset)
        self.screen.blit(surf, rect)
        return rect