import json

from colorthief import ColorThief
import requests


def get_color(img_url: str):
    color_thief = ColorThief(requests.get(img_url, stream=True).raw)
    dominant_color = color_thief.get_color(quality=1)

    def rgb2hex(r, g, b):
        return f"#{r:02x}{g:02x}{b:02x}"

    hexa = rgb2hex(dominant_color[0], dominant_color[1], dominant_color[2])
    hexa = hexa.replace("#", "")
    return int(hexa, 16)


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
