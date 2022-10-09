import discord
from discord.ext import commands
import subprocess
import json

from cogs.utils import is_dev

with open('secrets.json') as f:
    keys = json.load(f)

class DevCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in as {self.bot.user}')

    @commands.command()
    async def shutdown(self, ctx: commands.Context):
        if await is_dev(ctx.author):
            await ctx.send("Shutting down...")
            exit()

    @commands.command(
        name="restart",
        brief="Restarts bot, ***Dev use only***",
        help="Restarts bot, don't use if you're not a dev, will not work.",
    )
    async def restart(self, ctx: commands.Context):
        if await is_dev(ctx.author):
            await ctx.send("Restarting...")
            subprocess.call(keys["RUN_BOT"])

async def setup(bot: commands.Bot):
    await bot.add_cog(DevCog(bot))
