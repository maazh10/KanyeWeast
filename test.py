import json
import discord
from discord.ext import commands
import asyncio

f = open('secrets.json')
keys = json.load(f)

################################### "Common functions" ###################################

def is_dev(user: discord.abc.User) -> bool:
  """Checks if user is dev."""
  return str(user.id) == keys['ID_BENNY'] or str(user.id) == keys['ID_STARBOY']

##########################################################################################

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

bot = commands.Bot(command_prefix='&', help_command = help_command, intents=discord.Intents.all())

async def main():
  await bot.load_extension('cogs.dev')
  await bot.start(keys['TOKEN'])

asyncio.run(main())