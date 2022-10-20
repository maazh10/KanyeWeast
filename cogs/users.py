import discord
from discord.ext import commands
from discord.ext import buttons
from cogs.utils import is_dev

from random import randint
import asyncio

class MyPaginator(buttons.Paginator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @buttons.button(emoji='\u23FA')
    async def record_button(self, ctx, member):
        await ctx.send('This button sends a silly message! But could be programmed to do much more.')

    @buttons.button(emoji='my_custom_emoji:1234567890')
    async def silly_button(self, ctx, member):
        await ctx.send('Beep boop...')

class Users(commands.Cog):
    """This category has all commands where you can mention users."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

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
            if await is_dev(ctx.author):
                length = 30
            else:
                length = randint(0, 30)
        else:
            mem = await self.get_user(ctx, user)
            if await is_dev(mem): 
                length = 30
            else:
                length = randint(0, 30)
            user = mem.name
    
        penis = f"**{user}'s penis:**\n8"
        for i in range(length):
            penis += "="
        penis += "D\n"
        await ctx.send(penis)

    @commands.command()
    async def test(self, ctx: commands.Context):
        pagey = MyPaginator(title='Silly Paginator', colour=0xc67862, embed=True, timeout=90, use_defaults=True,
                        entries=[1, 2, 3], length=1, format='**')
        await pagey.start(ctx)

async def setup(bot: commands.Bot):
    await bot.add_cog(Users(bot))