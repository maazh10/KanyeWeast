import sqlite3

from PIL import Image
from discord.ext import commands
import requests


def get_color(image_url: str, palette_size=16) -> int:
    # https://stackoverflow.com/questions/3241929/python-find-dominant-most-common-color-in-an-image
    image = Image.open(requests.get(image_url, stream=True).raw)
    image.thumbnail((100, 100))
    paletted = image.convert("P", palette=Image.Palette.ADAPTIVE, colors=palette_size)

    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    palette_index = color_counts[0][1]
    dominant_color = palette[palette_index * 3 : palette_index * 3 + 3]
    return int(
        f"0x{dominant_color[0]:02x}{dominant_color[1]:02x}{dominant_color[2]:02x}", 16
    )


class UserBanned(commands.CommandError):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)


def category_map(name: str):
    categories = {
        "general": 9,
        "books": 10,
        "film": 11,
        "music": 12,
        "theatre": 13,
        "television": 14,
        "video games": 15,
        "board games": 16,
        "nature": 17,
        "computers": 18,
        "math": 19,
        "mythology": 20,
        "sports": 21,
        "geography": 22,
        "history": 23,
        "politics": 24,
        "art": 25,
        "celebrities": 26,
        "animals": 27,
        "vehicles": 28,
        "comics": 29,
        "gadgets": 30,
        "anime": 31,
        "cartoon": 32,
    }
    try:
        return categories[name]
    except KeyError:
        return None
