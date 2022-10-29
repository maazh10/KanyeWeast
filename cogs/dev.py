import discord
from discord.ext import commands
import subprocess
import json


class DevelopersOnly(commands.Cog):
    """This category is only for dev use. If you're not a dev and try to use you could be banned."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        with open("secrets.json") as f:
            self.keys = json.load(f)

    async def cog_check(self, ctx: commands.Context):
        return await self.bot.is_owner(ctx.author)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"We have logged in as {self.bot.user}")

    @commands.command()
    async def shutdown(self, ctx: commands.Context):
        await ctx.send("Shutting down...")
        exit()

    @commands.command()
    async def test(self, ctx: commands.Context):
        await ctx.send("Hello dev")

    @commands.command(
        name="restart",
        brief="Restarts bot, ***Dev use only***",
        help="Restarts bot, don't use if you're not a dev, will not work.",
    )
    async def restart(self, ctx: commands.Context):
        await ctx.send("Restarting...")
        subprocess.call(self.keys["RUN_BOT"])

    @commands.command(
        name="getgit",
        brief="Gets git info from latest commit.",
        help="Prints commit message and hash of current commit.",
    )
    async def getgit(self, ctx: commands.Context):
        await ctx.send(
            subprocess.check_output(["git", "log", "-1", "--format=%h %s"])
            .decode("ascii")
            .strip()
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(DevelopersOnly(bot))
