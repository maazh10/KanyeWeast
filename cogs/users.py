import discord
from discord.ext import commands

from random import randint
import asyncio

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

    @discord.ui.button(label="Red Button", style=discord.ButtonStyle.red)  # or .danger
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
            return await self.bot.fetch_user(int(user))

    @commands.command(
        name="annoy",
        brief="Annoys mentioned user",
        help="Pings mentioned user the number of times specified",
    )
    async def annoy(
        self,
        ctx: commands.Context,
        user: str = "",
        num_str: str = "",
        opt_str: str = "",
    ):
        invalid_num = False
        in_range = True
        invalid_user = user[0] != "<"
        num = 1
        pinged = None
        flag = False

        invalid_num = not num_str.isdigit()
        if not invalid_num:
            num = int(num_str)
            in_range = num >= 0 and num <= 69

        pinged = await self.get_user(ctx, user)

        if invalid_user or invalid_num or not in_range:
            await ctx.send(
                "Specified number of times is too annoying or invalid or invalid user <:Pepepunch:794437891648520224>"
            )
            num = 5
            pinged = await self.bot.fetch_user(ctx.author.id)

        annoy_string = (
            opt_str if opt_str else "get annoyed <:Pepepunch:794437891648520224>"
        )
        if num == 1:
            await asyncio.sleep(randint(0, 30))
            await ctx.send(f"{pinged.mention} {annoy_string}")
        else:
            for i in range(num):
                sleepnum = randint(0, 30)
                sleepnum = 0
                print(f"{sleepnum}, {pinged.display_name}, {num - i}")
                await asyncio.sleep(sleepnum)
                await ctx.send(
                    f"{pinged.mention} {annoy_string} {num - i}",
                    delete_after=10,
                )
        await ctx.send("Have a nice day :kissing_heart:")

    @commands.command(
        name="roast", brief="Roast user", help="Roasts the author or mentioned user."
    )
    async def roast(self, ctx: commands.Context, user: str = ""):
        with open("roasts.txt", "r") as f:
            lines = f.readlines()
            i = randint(0, len(lines))

        pinged = await self.get_user(ctx, user)
        await ctx.send(f"{pinged.mention}. {lines[i]}")

    @commands.command(
        aliases=["penis", "dick", "dagger", "glizzy", "ydd", "cock", "schlong"],
        brief="Shows your pp.",
        help="Shows your pp.",
    )
    async def pp(self, ctx: commands.Context, user=""):
        if user:
            mem = await self.get_user(ctx, user)
            user = mem.name
        else:
            mem = ctx.author
            user = ctx.message.author.name
        length = 30 if await self.bot.is_owner(mem) else randint(0, 30)

        penis = f"**{user}'s penis:**\n8{'=' * length}D"
        await ctx.send(penis)


async def setup(bot: commands.Bot):
    await bot.add_cog(Users(bot))
