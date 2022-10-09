import discord
from discord.ext import commands
import json

with open('secrets.json') as f:
    keys = json.load(f)

async def is_dev(user: discord.abc.User) -> bool:
    """Checks if user is dev."""
    return str(user.id) == keys['ID_BENNY'] or str(user.id) == keys['ID_STARBOY']