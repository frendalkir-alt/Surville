"""Настройки."""

WINDOW_TITLE = "Surville"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
BACKGROUND_COLOR = (12, 20, 30)
DEBUG = False

# --- Игрок ---
PLAYER_WALK_SPEED = 190.0
PLAYER_RUN_SPEED = 320.0
PLAYER_RADIUS = 12
PLAYER_MAX_HP = 100.0
PLAYER_MAX_HUNGER = 100.0
PLAYER_MAX_THIRST = 100.0
PLAYER_MAX_STAMINA = 100.0

HUNGER_DECAY = 0.55          # единиц в секунду
THIRST_DECAY = 0.85
STARVING_DAMAGE = 2.5        # HP/сек, если голод или жажда = 0
STAMINA_DRAIN = 28.0
STAMINA_REGEN = 16.0

PLAYER_INVULN_ON_HIT = 0.6

# --- Мир ---
TILE_SIZE = 64
WORLD_TILES_X = 64
WORLD_TILES_Y = 64
WORLD_SEED = 1337

# --- Взаимодействие ---
INTERACT_RADIUS = 56.0

# --- День/ночь ---
DAY_DURATION = 240.0         # полный цикл в секундах
NIGHT_START = 0.65           # 65% цикла = ночь
NIGHT_COLOR = (10, 15, 40)
NIGHT_MAX_ALPHA = 170

# --- Цвета тайлов (fallback пока нет спрайтов) ---
BIOME_COLORS = {
    "water":  (40, 90, 160),
    "beach":  (222, 205, 150),
    "grass":  (110, 170, 90),
    "jungle": (60, 120, 70),
    "rock":   (130, 130, 130),
}