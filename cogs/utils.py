import json

from colorthief import ColorThief
import requests


async def get_color(img_url: str):
    color_thief = ColorThief(requests.get(img_url, stream=True).raw)
    dominant_color = color_thief.get_color(quality=1)
    def rgb2hex(r, g, b): return f"#{r:02x}{g:02x}{b:02x}"
    hexa = rgb2hex(dominant_color[0], dominant_color[1], dominant_color[2])
    hexa = hexa.replace("#", "")
    return int(hexa, 16)
