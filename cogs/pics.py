import discord
from discord.ext import commands

import os
import random
import requests
import shutil
import string
from pathlib import Path


class Pictures(commands.Cog):
    """All your pic related commands lie here."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.base_directory = os.path.abspath(os.curdir)
        self.pics_directory = os.path.abspath(os.path.join(os.curdir, "pics"))

    async def get_stats(self, ctx: commands.Context):
        os.chdir(self.pics_directory)
        homies = [
            (homie, len(os.listdir(homie)))
            for homie in os.listdir(os.curdir)
            if not (
                homie.startswith(".")
                or homie == "amogus"
                or homie == "hbk"
                or homie == "haram"
            )
        ]
        msg = "```\n"
        sorted_homies = sorted(homies, key=lambda d: d[1], reverse=True)
        for homie in [homie[0] for homie in sorted_homies]:
            msg += f"{homie} {len(os.listdir(homie))}\n"
        msg += "```"
        os.chdir(self.base_directory)
        await ctx.send(msg)

    # @commands.command(
    #     name="homienum",
    #     brief="Sends nth pic of homie from modification date",
    #     help="Use &homienum name [num] to get specific pic, Gets latest pic by default.",
    # )
    async def get_num(self, ctx: commands.Context, name: str = "", num: int = -1):
        if name == "":
            await ctx.send("Must provide name.")
            return
        if name not in [
            x
            for x in os.listdir(self.pics_directory)
            if not (x.startswith(".") or x == "amogus" or x == "hbk" or x == "haram")
        ]:
            await ctx.send("Invalid homie.")
            return
        os.chdir(os.path.join(self.pics_directory, name))
        sorted_list = sorted(Path(".").iterdir(),
                             key=lambda f: f.stat().st_ctime)
        sorted_list = [
            x for x in sorted_list if not x.parts[-1].startswith(".")]
        if num != 0 and num >= len(sorted_list):
            await ctx.send("Not a valid number")
            # TODO: Maybe ask if user wants to mod the number to return something in the future
            return
        await ctx.send(file=discord.File(sorted_list[num]), delete_after=5)
        os.chdir(self.base_directory)

    async def get_homie_stat(self, ctx: commands.Context, name: str):
        if name not in [
            x
            for x in os.listdir(self.pics_directory)
            if not (x.startswith(".") or x == "amogus" or x == "hbk" or x == "haram")
        ]:
            await ctx.send("Invalid homie.")
            return
        msg = f"```{name} {len(os.listdir(os.path.join(self.pics_directory, name)))}```"
        await ctx.send(msg)

    @commands.command(
        name="homie",
        brief="Sends random homie pic",
        help="Send random homie pic. Use &homie [homie name] [opt]. Use &homie list for a list of names. Or &homie stats for stats on homie pics. Picks random homie if no arguement provided. Use opt to provide specific picture in database, or latest to get latest picture",
    )
    async def homies(self, ctx: commands.Context, homie="", opt=""):
        match homie:
            case "stats":
                await self.get_stats(ctx)
                return
            case "aritzia":
                homie = "irtiza"
            case "list":
                await self.list(ctx)
                return
            case _:
                pass

        if opt == "latest":
            opt = "-1"

        if opt == "stats":
            await self.get_homie_stat(ctx, homie)
            return

        homies = os.listdir(self.pics_directory)
        try:
            homies.remove("amogus")
            homies.remove("hbk")
            homies.remove("haram")
        except ValueError as err:
            print(f"ValueError: {err}")
        if not homie:
            i = random.randint(0, len(homies) - 1)
            folder = os.path.join("pics", homies[i])
        else:
            if homie.lower() in homies:
                folder = os.path.join("pics", homie.lower())
            else:
                await ctx.send("invalid homie")
                return
        if opt.isdigit() or opt == "-1":
            await self.get_num(ctx, homie, int(opt))
            return
        images = os.listdir(folder)
        j = random.randint(0, len(images) - 1)
        await ctx.send(
            file=discord.File(os.path.join(folder, images[j])), delete_after=5
        )

    async def list(self, ctx: commands.Context):
        homies = [
            homie
            for homie in os.listdir(self.pics_directory)
            if not (
                homie.startswith(".")
                or homie == "amogus"
                or homie == "hbk"
                or homie == "haram"
            )
        ]
        msg = "```\n"
        for homie in homies:
            msg += homie + "\n"
        msg += "```"
        await ctx.send(msg)

    @ commands.command(
        name="homir",
        brief="Sends homie pic of mir",
        help="Easy mir spamming for your enjoyment :)",
    )
    async def homir(self, ctx: commands.Context, opt: str = ""):
        await self.homies(ctx, "mir", opt)

    @ commands.command(
        name="homo",
        brief="Sends homie pic of null",
        help="Easy null spamming for your enjoyment :)",
    )
    async def homo(self, ctx: commands.Context, opt: str = ""):
        await self.homies(ctx, "mo", opt)

    async def save_pic(self, name: str, url: str):
        folder = os.path.join(self.pics_directory, name)
        img_data = requests.get(url).content
        img_name = (
            "".join(random.choices(string.ascii_uppercase + string.digits, k=18))
            + ".jpg"
        )
        path = os.path.join(folder, img_name)
        with open(path, "wb") as handler:
            handler.write(img_data)

    @ commands.command(
        name="addpic",
        brief="Adds a new image to specified folder(s).",
        help="Add a new image by adding the image as an attachment and specifying a folder location(s) (homie name) or amogus for sus quotes. &addpic {foldername} {foldername} ... {foldername}",
    )
    async def addpic(self, ctx: commands.Context, *folders):
        if not folders:
            await ctx.send("please specify folder(s).")
            return
        if len(ctx.message.attachments) == 0:
            await ctx.send("attach an image to be added.")
            return
        for name in folders:
            if name not in os.listdir(self.pics_directory):
                await ctx.send(
                    f"folder {name} does not exist. use &addfolder to create."
                )
            else:
                for attachment in ctx.message.attachments:
                    await self.save_pic(name, attachment.url)
                await ctx.send(
                    f"image{'s' * (len(ctx.message.attachments) > 1)} added to {name}."
                )

    @ commands.command(
        name="addfolder",
        brief="Adds new folder to pics.",
        help="Adds a new folder to be used for &homies. (dev only)",
    )
    async def addfolder(self, ctx: commands.Context, folder=""):
        if not await self.bot.is_owner(ctx.author):
            await ctx.send("this command is dev only pleb.")
            return
        if folder == "":
            await ctx.send("please specify a folder.")
            return
        if folder in os.listdir("pics"):
            await ctx.send("folder already exists.")
            return
        os.mkdir(os.path.join("pics", folder))
        await ctx.send(f"folder {folder} added. use &addpic {folder} to add images.")

    @ commands.command(
        name="rmfolder",
        brief="Removes a folder from pics.",
        help="Removes a folder from pics. (dev only)",
    )
    async def rmfolder(self, ctx: commands.Context, folder=""):
        if not await self.bot.is_owner(ctx.author):
            await ctx.send("this command is dev only pleb.")
            return
        if folder == "":
            await ctx.send("please specify a folder.")
            return
        if folder not in os.listdir("pics"):
            await ctx.send("folder does not exist.")
            return
        if len(os.listdir(os.path.join("pics", folder))) == 0:
            shutil.rmtree(os.path.join("pics", folder))
            await ctx.send(f"folder {folder} removed.")
            return
        await ctx.send(f"folder {folder} not removed beacuse it's non-empty.")

    @ commands.command(
        name="amogus",
        brief="Sends sus message from server.",
        help="Sends random sus message from server.",
    )
    async def sus(self, ctx: commands.Context):
        images = os.listdir("pics/amogus")
        i = random.randint(0, len(images) - 1)
        await ctx.send(file=discord.File(os.path.join("pics/amogus", images[i])))

    @ commands.command(
        name="haram",
        brief="Sends haram accusation.",
        help="Sends random sus message from server.",
    )
    async def haram(self, ctx: commands.Context):
        images = os.listdir("pics/haram")
        i = random.randint(0, len(images) - 1)
        await ctx.send(file=discord.File(os.path.join("pics/haram", images[i])))

    @ commands.command(
        aliases=["sad"],
        brief="Sends heartbroken quote/image.",
        help="Sends heartbroken quote/image.",
    )
    async def hbk(self, ctx: commands.Context):
        images = os.listdir("pics/hbk")
        i = random.randint(0, len(images) - 1)
        file = discord.File(os.path.join("pics/hbk", images[i]))
        text = images[i][:-3]
        if len(text) >= 40:
            await ctx.send(text, file=file)
        else:
            await ctx.send(file=file)


async def setup(bot: commands.Bot):
    await bot.add_cog(Pictures(bot))
