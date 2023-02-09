import discord
from discord.ext import commands

from cogs.utils import UserBanned
from random import randint
import asyncio
import sys
import traceback
from typing import Annotated

########################################################################


class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(
        label="Blurple Button", style=discord.ButtonStyle.blurple
    )  # or .primary
    async def blurple_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(
        label="Gray Button", style=discord.ButtonStyle.gray
    )  # or .secondary/.grey
    async def gray_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(
        label="Green Button", style=discord.ButtonStyle.green
    )  # or .success
    async def green_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        button.disabled = True
        await interaction.response.edit_message(view=self)

    # or .danger
    @discord.ui.button(label="Red Button", style=discord.ButtonStyle.red)
    async def red_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        button.disabled = True
        await interaction.response.edit_message(view=self)


########################################################################


class Users(commands.Cog):
    """This category has all commands where you can mention users."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="button")
    async def button(self, ctx: commands.Context):
        view = Buttons()
        view.add_item(
            discord.ui.Button(
                label="URL Button",
                style=discord.ButtonStyle.link,
                url="https://github.com/lykn",
            )
        )
        await ctx.send("This message has buttons!", view=view)

    async def get_user(self, ctx: commands.Context, user: str) -> discord.abc.User:
        if not user:
            # fallsback to author if no user is provided
            return ctx.author
        if ctx.message.mentions:
            return ctx.message.mentions[0]
        if user.isdigit():
            return await self.bot.fetch_user(int(user))
        else:
            user = user.replace("<", "")
            user = user.replace(">", "")
            user = user.replace("@", "")
            try:
                return await self.bot.fetch_user(int(user))
            finally:
                return ctx.author

    ##################################################################################################
    ###################################### GLOBAL ERROR HANDLER ######################################
    ##################################################################################################

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error: commands.CommandError):
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, "on_error"):
            return

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

    ##################################################################################################
    ######################################## COG BAN CHECK ###########################################
    ##################################################################################################
    
    async def cog_check(self, ctx: commands.Context) -> bool:
        dev = self.bot.get_cog("DevelopersOnly")
        if ctx.author in dev.banned_set:
            raise UserBanned(ctx.message.author)
        return True

    ##################################################################################################
    ##################################### CUSTOM USER CONVERTER ######################################
    ##################################################################################################

    class BennysUserConverter(commands.UserConverter):
        async def convert(self, ctx, argument) -> discord.abc.User:
            try:
                user = await super().convert(ctx, argument)
                return user
            except commands.UserNotFound as error:
                traceback.print_exception(
                    type(error), error, error.__traceback__, file=sys.stderr
                )
                return ctx.author

    ##################################################################################################

    async def annoy_logic(
        self,
        ctx: commands.Context,
        user: discord.abc.User,
        num: int = 1,
        opt_str: str = "",
    ):
        annoy_string = (
            opt_str if opt_str else "get annoyed <:Pepepunch:794437891648520224>"
        )
        if num == 1:
            await asyncio.sleep(randint(0, 30))
            await ctx.send(f"{user.mention} {annoy_string}", delete_after=10)
        else:
            for i in range(num):
                sleepnum = randint(0, 30)
                print(f"{sleepnum}, {user.display_name}, {num - i}")
                await asyncio.sleep(sleepnum)
                await ctx.send(
                    f"{user.mention} {annoy_string} {num - i}",
                    delete_after=10,
                )
        await ctx.send("Have a nice day :kissing_heart:")

    @commands.command(
        name="annoy",
        brief="Annoys mentioned user",
        help="Pings mentioned user the number of times specified",
    )
    async def annoy_parse(
        self,
        ctx: commands.Context,
        user: Annotated[discord.User, BennysUserConverter],
        num: commands.Range[int, 0, 69] = 1,
        opt_str: str = "",
    ):
        await self.annoy_logic(ctx, user, num, opt_str)

    @annoy_parse.error
    async def annoy_error(self, ctx: commands.Context, e: commands.CommandError):
        if isinstance(e, commands.RangeError):
            await ctx.send("Specified number is out of range")
        if isinstance(e, commands.BadArgument):
            await ctx.send("Argument cannot be converted")
        print(type(e).__name__, repr(e))

        await ctx.send(
            "Specified number of times is too annoying or invalid or invalid user <:Pepepunch:794437891648520224>"
        )
        await self.annoy_logic(ctx, ctx.message.author, 5)

    @commands.command(
        name="roast", brief="Roast user", help="Roasts the author or mentioned user."
    )
    async def roast(
        self,
        ctx: commands.Context,
        user: Annotated[discord.User, BennysUserConverter] = commands.Author,
    ):
        with open("roasts.txt", "r") as f:
            lines = f.readlines()
            i = randint(0, len(lines))

        await ctx.send(f"{user.mention}. {lines[i]}")

    @commands.command(
        aliases=["penis", "dick", "dagger", "glizzy", "ydd", "cock", "schlong"],
        brief="Shows your pp.",
        help="Shows your pp.",
    )
    async def pp(
        self,
        ctx: commands.Context,
        user: Annotated[discord.User, BennysUserConverter] = commands.Author,
    ):
        length = 30 if await self.bot.is_owner(user) else randint(0, 30)
        penis = f"**{user.display_name}'s penis:**\n8{'=' * length}D"
        await ctx.send(penis)


async def setup(bot: commands.Bot):
    await bot.add_cog(Users(bot))
