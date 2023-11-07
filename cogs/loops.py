import discord
from discord.ext import commands, tasks

from cogs.utils import get_quote


class Loops(commands.Cog):
    """All async loops for the bot"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    ##############################
    ####### COG BAN CHECK ########
    ##############################

    async def cog_check(self, ctx: commands.Context) -> bool:
        return await self.bot.is_owner(ctx.author)

    ##############################
    ##############################
    ##############################

    def cog_unload(self) -> None:
        self.status.cancel()

    @tasks.loop(hours=1)
    async def status(self) -> None:
        await self.bot.change_presence(
            activity=discord.Game(
                name=get_quote(),
            )
        )

    @status.before_loop
    async def before_status(self) -> None:
        await self.bot.wait_until_ready()

    @commands.command(
        name="status",
        brief="Starts the status loop",
        help="Starts the status loop",
    )
    async def status_command(self, ctx: commands.Context) -> None:
        self.status.start()
        await ctx.send("Status loop started")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Loops(bot))
