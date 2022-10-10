import discord
import json

from colorthief import ColorThief
import requests

with open('secrets.json') as f:
    keys = json.load(f)

async def is_dev(user: discord.abc.User) -> bool:
    """Checks if user is dev."""
    return str(user.id) == keys['ID_BENNY'] or str(user.id) == keys['ID_STARBOY']

async def get_color(self, img_url: str):
    color_thief = ColorThief(requests.get(img_url, stream=True).raw)
    dominant_color = color_thief.get_color(quality=1)
    rgb2hex = lambda r,g,b: f"#{r:02x}{g:02x}{b:02x}"
    hexa = rgb2hex(dominant_color[0],dominant_color[1],dominant_color[2])
    hexa = hexa.replace("#","")
    return int(hexa, 16)
