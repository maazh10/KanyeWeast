import logging
import sys
import traceback

import discord
from discord.ext import commands

from cogs.utils import UserBanned

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
            # This prevents any commands with local handlers being handled here in on_command_error.
            if hasattr(ctx.command, "on_error"):
                return

            # TODO: make an actual global error handler that uses this if block
            # This prevents any cogs with an overwritten cog_command_error being handled here.
            cog = ctx.cog
            if cog:
                if cog._get_overridden_method(cog.cog_command_error) is not None:
                    return

            ignored = ()

            # Allows us to check for original exceptions raised and sent to CommandInvokeError.
            # If nothing is found. We keep the exception passed to on_command_error.
            error = getattr(error, "original", error)

            # Anything in ignored will return and prevent anything happening.
            if isinstance(error, ignored):
                return

            if isinstance(error, UserBanned):
                await ctx.send("You are banned.")
                return

            if isinstance(error, commands.DisabledCommand):
                await ctx.send(f"{ctx.command} has been disabled.")

            elif isinstance(error, commands.NoPrivateMessage):
                try:
                    await ctx.author.send(
                        f"{ctx.command} can not be used in Private Messages."
                    )
                except discord.HTTPException:
                    pass

            # For this error example we check to see where it came from...
            elif isinstance(error, commands.BadArgument):
                await ctx.send("Bad Argument provided.")

            elif isinstance(error, commands.UserNotFound):
                await ctx.send("No user found. Try again")

            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send("Missing required argument. Try again")

            else:
                # All other Errors not returned come here. And we can just print the default TraceBack.
                print(
                    "Ignoring exception in command {}:".format(ctx.command), file=sys.stderr
                )
                traceback.print_exception(
                    type(error), error, error.__traceback__, file=sys.stderr
                )
                logger = logging.getLogger("discord")
                logger.error(
                    "Ignoring exception in command {}:".format(ctx.command),
                    exc_info=(type(error), error, error.__traceback__),
                )
            return

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        logging.getLogger("discord").info(f"Command {ctx.command.name} was used by {ctx.author} with args {ctx.args} and kwargs {ctx.kwargs}")

async def setup(bot: commands.Bot):
    await bot.add_cog(CommandErrorHandler(bot))
