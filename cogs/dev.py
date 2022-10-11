import discord
from discord.ext import commands
import subprocess
import json

from cogs.utils import is_dev


class DevelopersOnly(commands.Cog):
    """This category is only for dev use. If you're not a dev and try to use you could be banned."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        with open('secrets.json') as f:
            self.keys = json.load(f)

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
            subprocess.call(self.keys["RUN_BOT"])

async def setup(bot: commands.Bot):
    await bot.add_cog(DevelopersOnly(bot))
