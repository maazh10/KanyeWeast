import asyncio
import random
import sys
import traceback
from random import randint
from secrets import randbelow
from typing import Annotated

import discord
import requests
from discord.ext import commands

from cogs.dev import DevelopersOnly
from cogs.utils import UserBanned

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
    ### CUSTOM USER CONVERTER ####
    ##############################

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

    ##############################

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
        if isinstance(e, UserBanned):
            await ctx.send("You are banned.")
            return
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
        if randint(0, 1) < 0.2:
            with open("roasts.txt", "r") as f:
                lines = f.readlines()
                i = randint(0, len(lines))
            await ctx.send(f"{user.mention}. {lines[i]}")
        else:
            res = requests.get(
                "https://evilinsult.com/generate_insult.php?lang=en&type=json"
            )
            await ctx.send(f"{user.mention}. {res.json()['insult']}")

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
        # length = randint(0, 30)
        length = randbelow(31)
        # length = 30 if await self.bot.is_owner(user) else randint(0, 30)
        # if (user.id == 356493485030768640):
        #     length = randint(0, 8)
        penis = f"**{user.display_name}'s penis:**\n8{'=' * length}D"
        await ctx.send(penis)

    @commands.command(
        name="",
        brief="Sends a pickup line",
        help="Sends a pickup line for the mentioned user",
    )
    async def rizz(
        self,
        ctx: commands.Context,
        user: Annotated[discord.User, BennysUserConverter] = commands.Author,
    ):
        res = requests.get("https://vinuxd.vercel.app/api/pickup")
        line = res.json()["pickup"]
        if user == ctx.author:
            await ctx.send(line)
            return
        emojis = [
            "<:cozysip_blob:879363563062435840>",
            "<:8850_peepoHappyLove:763501999865856060>",
            ":smiling_face_with_3_hearts:",
            ":heart:",
            "<:red_blob:879363248380575745>",
            ":flushed:",
        ]
        await ctx.send(f"{user.mention}, {line} {random.choice(emojis)}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Users(bot))
