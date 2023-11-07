import discord
from discord.ext import commands

from cogs.dev import DevelopersOnly
from cogs.utils import UserBanned


class __COG_NAME__(commands.Cog):
    """__COG_DESCRIPTION__"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    ##############################
    ####### COG BAN CHECK ########
    ##############################

    async def cog_check(self, ctx: commands.Context) -> bool:
        dev = self.bot.get_cog("DevelopersOnly")
        assert isinstance(dev, DevelopersOnly)
        if ctx.author.id in dev.banned_set:
            raise UserBanned(ctx.message.author)
        return True

    ##############################
    ##############################
    ##############################

    # Add your commands here
    @commands.command(
        name="__COMMAND_NAME__",
        aliases=["__COMMAND_ALIAS__"],
        brief="__COMMAND_BRIEF__",
        help="__COMMAND_DESCRIPTION__",
    )
    async def __COMMAND_NAME__(self, ctx: commands.Context):
        await ctx.send("Hello World!")


async def setup(bot: commands.Bot):
    await bot.add_cog(__COG_NAME__(bot))
