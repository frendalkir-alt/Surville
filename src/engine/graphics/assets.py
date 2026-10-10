"""Загрузка и кэширование ресурсов."""
import pygame

from ..utils.paths import ASSETS_DIR
from ..utils.logger import get_logger

log = get_logger("assets")


class AssetManager:
    def __init__(self):
        self._images = {}
        self._sounds = {}
        self._fonts = {}

    def has_image(self, relative_path) -> bool:
        return (ASSETS_DIR / relative_path).exists()

    def image(self, relative_path, size=None, fallback_color=(255, 0, 255)):
        key = (str(relative_path), size)
        if key in self._images:
            return self._images[key]

        full = ASSETS_DIR / relative_path
        if full.exists():
            surf = pygame.image.load(str(full)).convert_alpha()
            if size:
                surf = pygame.transform.scale(surf, size)
        else:
            log.warning("Missing image: %s (placeholder)", relative_path)
            surf = self._placeholder(size or (32, 32), fallback_color)

        self._images[key] = surf
        return surf

    def load_frames(self, relative_path, frame_width, frame_height, count=None):
        """Режет спрайтшит на кадры слева-направо, сверху-вниз."""
        sheet = self.image(relative_path)
        cols = max(1, sheet.get_width() // frame_width)
        rows = max(1, sheet.get_height() // frame_height)
        total = cols * rows
        if count is not None:
            total = min(total, count)

        frames = []
        for i in range(total):
            x = (i % cols) * frame_width
            y = (i // cols) * frame_height
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (x, y, frame_width, frame_height))
            frames.append(frame)
        return frames

    def sound(self, relative_path):
        if relative_path in self._sounds:
            return self._sounds[relative_path]

        full = ASSETS_DIR / relative_path
        snd = None
        if full.exists():
            if hasattr(pygame, "mixer") and pygame.mixer.get_init():
                try:
                    snd = pygame.mixer.Sound(str(full))
                except Exception as e:
                    log.warning("Sound load failed: %s (%s)", relative_path, e)
            else:
                log.warning("Sound skipped (no mixer): %s", relative_path)
        else:
            log.warning("Missing sound: %s", relative_path)

        self._sounds[relative_path] = snd
        return snd

    def font(self, name, size):
        key = (name, size)
        if key in self._fonts:
            return self._fonts[key]
        try:
            f = pygame.font.Font(name, size) if name else pygame.font.Font(None, size)
        except (FileNotFoundError, pygame.error):
            f = pygame.font.Font(None, size)
        self._fonts[key] = f
        return f

    @staticmethod
    def _placeholder(size, color):
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill(color)
        pygame.draw.rect(surf, (0, 0, 0), surf.get_rect(), 2)
        return surf


# глобальный инстанс для удобства
assets = AssetManager()