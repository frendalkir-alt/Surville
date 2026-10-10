"""Управление звуком и музыкой. Устойчиво к отсутствию pygame.mixer."""
import pygame

from ..utils.logger import get_logger

log = get_logger("audio")


def _mixer_available():
    """Проверяем, есть ли вообще pygame.mixer в этой сборке."""
    return hasattr(pygame, "mixer")


class AudioManager:
    def __init__(self, master_volume=0.8):
        self.master_volume = master_volume
        self.music_volume = 0.5
        self.sfx_volume = 0.8
        self.enabled = False

    def init(self):
        if not _mixer_available():
            log.warning("pygame.mixer недоступен — играем без звука")
            return
        try:
            pygame.mixer.init()
            self.enabled = True
        except (pygame.error, NotImplementedError) as e:
            log.warning("Mixer init failed: %s — играем без звука", e)

    def play_sound(self, sound):
        if not self.enabled or sound is None:
            return
        try:
            sound.set_volume(self.sfx_volume * self.master_volume)
            sound.play()
        except Exception as e:
            log.warning("play_sound failed: %s", e)

    def play_music(self, path, loops=-1):
        if not self.enabled:
            return
        try:
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
            pygame.mixer.music.play(loops)
        except Exception as e:
            log.warning("Music failed: %s", e)

    def stop_music(self):
        if not self.enabled:
            return
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass


audio = AudioManager()