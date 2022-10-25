import discord
from discord.ext import commands

from random import randint
import asyncio

########################################################################

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout = timeout)

    @discord.ui.button(label = "Blurple Button", style = discord.ButtonStyle.blurple) # or .primary
    async def blurple_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled=True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label = "Gray Button", style = discord.ButtonStyle.gray) # or .secondary/.grey
    async def gray_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled=True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label = "Green Button", style = discord.ButtonStyle.green) # or .success
    async def green_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled=True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label = "Red Button", style = discord.ButtonStyle.red) # or .danger
    async def red_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled=True
        await interaction.response.edit_message(view=self)



########################################################################

class Users(commands.Cog):
    """This category has all commands where you can mention users."""
    
    

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="button")
    async def button(self, ctx: commands.Context):
        view=Buttons()
        view.add_item(discord.ui.Button(label="URL Button",style=discord.ButtonStyle.link,url="https://github.com/lykn"))
        await ctx.send("This message has buttons!",view=view)

    async def get_user(self, ctx: commands.Context, user: str | None) -> discord.abc.User:
        if user == None:
            print("not enough arguments")
            return ctx.author
        if ctx.message.mentions:
            return ctx.message.mentions[0]
        if user.isdigit():
            return await self.bot.fetch_user(int(user))
        else:
            user = user.replace("<","")
            user = user.replace(">","")
            user = user.replace("@","")
            return await self.bot.fetch_user(int(user))

    @commands.command(name="annoy", 
    brief="Annoys mentioned user", 
    help="Pings mentioned user the number of times specified")
    async def annoy(self, ctx: commands.Context, user = None, num_str = None, opt_str = None):
        invalid_num = False
        in_range = True
        invalid_user = user[0] != "<"
        if num_str != None:
            invalid_num = not num_str.isdigit()
            if (not invalid_num):
                num = int(num_str)
                if (num > 69 or num < 0):
                    in_range = False
        else:
            num = 1

        flag = False
        if user[0] == "<":
            print(user[2:-1])
            pinged = await self.bot.fetch_user(user[2:-1])
            flag = True

        if invalid_user or invalid_num or not in_range:
            await ctx.send("Specified number of times is too annoying or invalid or invalid user <:Pepepunch:794437891648520224>")
            num = 5
            user = await self.bot.fetch_user(ctx.author.id)

        annoy_string = "get annoyed <:Pepepunch:794437891648520224>" if (opt_str == None) else " " + opt_str
        if num == 1:
            await ctx.send(user + annoy_string)
        else:
            for i in range(num):
                sleepnum = randint(0, 30)
                print(f"{sleepnum}, {pinged.display_name}, {num - i}") if flag else print(f"{sleepnum}, {user}, {num - i}")
                await asyncio.sleep(sleepnum)
                if invalid_user or invalid_num or not in_range:
                    await ctx.send(user.mention + annoy_string + " " + str(num-i), delete_after=10)
                else:
                    await ctx.send(user + annoy_string + " " + str(num-i), delete_after=10)

        await ctx.send("Have a nice day :kissing_heart:")
    

    @commands.command(name="roast",
    brief="Roast user",
    help="Roasts the author or mentioned user.")
    async def roast(self, ctx: commands.Context, user=None):
        with open("roasts.txt", "r") as f:
            lines = f.readlines()
            i = randint(0,len(lines))
        if user == None:
            await ctx.send(ctx.author.mention + ". " + lines[i])
        else:
            await ctx.send(user + ". " + lines[i])
 

    @commands.command(aliases=["penis", "dick", "dagger", "glizzy", "ydd", "cock", "schlong"],
    brief="Shows your pp.",
    help="Shows your pp.")
    async def pp(self, ctx: commands.Context, user=""):
        if user == "":
            user = ctx.message.author.name
            if await self.bot.is_owner(ctx.author):
                length = 30
            else:
                length = randint(0, 30)
        else:
            mem = await self.get_user(ctx, user)
            if await self.bot.is_owner(mem): 
                length = 30
            else:
                length = randint(0, 30)
            user = mem.name
    
        penis = f"**{user}'s penis:**\n8"
        for i in range(length):
            penis += "="
        penis += "D\n"
        await ctx.send(penis)

async def setup(bot: commands.Bot):
    await bot.add_cog(Users(bot))