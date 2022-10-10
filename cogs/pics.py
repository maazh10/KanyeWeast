import discord
from discord.ext import commands
from cogs.utils import is_dev

import os
import random
import requests
import shutil
import string

class Pictures(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.pics_directory = "../pics"

    @commands.command(name="homie",
    brief="Sends random homie pic",
    help="Send random homie pic. Use &homie [homie name]. Use &listhomies for a list of names. Picks random homie if no arguement provided.")
    async def homies(self, ctx: commands.Context, homie=""):
        homies = os.listdir(self.pics_directory) # not sure how os cd works with cogs as yet
        try:
            homies.remove('amogus')
            homies.remove('hbk')
            homies.remove('haram')
        except ValueError as err:
            print(f"ValueError: {err}") 
        if not homie:
            i = random.randint(0,len(homies)-1)
            folder = os.path.join('pics', homies[i])
        else:
            if homie.lower() in homies:
                folder = os.path.join('pics', homie.lower())
            else:
                await ctx.send("invalid homie")
                return
        images = os.listdir(folder)
        j = random.randint(0,len(images)-1)
        await ctx.send(file=discord.File(os.path.join(folder,images[j])), delete_after=5)

    @commands.command(name="listhomies",
    brief="Lists homies",
    help="Prints list of homies currently in our directory for &homie.")
    async def list(self, ctx: commands.Context, homie=""):
        homies = os.listdir('pics')
        try:
            homies.remove('amogus')
            homies.remove('hbk')
            homies.remove('haram')
        except ValueError as err:
            print(f"ValueError: {err}")
        msg = "```\n"
        for homie in homies:
            msg += homie + "\n"
        msg += "```"
        await ctx.send(msg)

    @commands.command(name="homir",
    brief="Sends homie pic of mir",
    help="Easy mir spamming for your enjoyment :)")
    async def homir(self, ctx: commands.Context):
        await self.homies(ctx, 'mir')

    @commands.command(name="homo",
    brief="Sends homie pic of null",
    help="Easy null spamming for your enjoyment :)")
    async def homo(self, ctx: commands.Context):
        await self.homies(ctx, 'mo')

    @commands.command(name="addpic",
    brief="Adds a new image to specified folder(s).",
    help="Add a new image by adding the image as an attatchment and specifying a folder location(s) (homie name) or amogus for sus quotes. &addpic {foldername} {foldername} ... {foldername}")
    async def addpic(self, ctx: commands.Context, *folders):
        if not folders:
            await ctx.send("please specify folder(s).")
            return
        if len(ctx.message.attachments) == 0:
            await ctx.send("attach an image to be added.")
            return
        if len(ctx.message.attachments) > 1:
            await ctx.send("too many attachments.")
            return
        for name in folders:
            if name not in os.listdir('pics'):
                await ctx.send(f"folder {name} does not exist. use &addfolder to create.")
            else:
                folder = os.path.join('pics', name)
                image_url = ctx.message.attachments[0].url
                img_data = requests.get(image_url).content
                img_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=18)) + '.jpg'
                path = os.path.join(folder, img_name)
                with open(path, 'wb') as handler:
                    handler.write(img_data)
                await ctx.send(f"image added to {name}.")

    @commands.command(name="addfolder",
    brief="Adds new folder to pics.",
    help="Adds a new folder to be used for &homies.")
    async def addfolder(self, ctx: commands.Context, folder=""):
        if folder == "":
            await ctx.send("please specify a folder.")
            return
        if folder in os.listdir('pics'):
            await ctx.send("folder already exists.")
            return
        os.mkdir(os.path.join('pics', folder))
        await ctx.send(f"folder {folder} added. use &addpic {folder} to add images.")

    @commands.command(name="rmfolder",
    brief="Removes a folder from pics.",
    help="Removes a folder from pics. (dev only)")
    async def rmfolder(self, ctx: commands.Context, folder=""):
        if not await is_dev(ctx.author):
            await ctx.send("this command is dev only pleb.")
            return
        if folder == "":
            await ctx.send("please specify a folder.")
            return
        if folder not in os.listdir('pics'):
            await ctx.send("folder does not exist.")
            return
        if len(os.listdir(os.path.join('pics', folder))) == 0:
            shutil.rmtree(os.path.join('pics', folder))
            await ctx.send(f"folder {folder} removed.")
            return
        await ctx.send(f"folder {folder} not removed beacuse it's non-empty.")

    @commands.command(name="amogus",
    brief="Sends sus message from server.",
    help="Sends random sus message from server.")
    async def sus(self, ctx: commands.Context):
        images = os.listdir('pics/amogus')
        i = random.randint(0,len(images)-1)
        await ctx.send(file=discord.File(os.path.join('pics/amogus',images[i])))

    @commands.command(name="haram",
    brief="Sends haram accusation.",
    help="Sends random sus message from server.")
    async def haram(self, ctx: commands.Context):
        images = os.listdir('pics/haram')
        i = random.randint(0,len(images)-1)
        await ctx.send(file=discord.File(os.path.join('pics/haram',images[i])))

    @commands.command(aliases=["sad"],
    brief="Sends heartbroken quote/image.",
    help="Sends heartbroken quote/image.")
    async def hbk(self, ctx: commands.Context):
        images = os.listdir('pics/hbk')
        i = random.randint(0,len(images)-1)
        file = discord.File(os.path.join('pics/hbk',images[i]))
        text = images[i][:-3]
        if len(text) >= 40:
            await ctx.send(text, file=file)
        else:
            await ctx.send(file=file)

async def setup(bot: commands.Bot):
    await bot.add_cog(Pictures(bot))