"""Пути к папкам проекта."""
from pathlib import Path

# .../Surville
BASE_DIR = Path(__file__).resolve().parents[3]
ASSETS_DIR = BASE_DIR / "assets"
LEVELS_DIR = BASE_DIR / "levels"


def asset_path(*parts) -> Path:
    return ASSETS_DIR.joinpath(*parts)


def level_path(*parts) -> Path:
    return LEVELS_DIR.joinpath(*parts)