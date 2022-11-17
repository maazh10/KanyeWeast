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
        self.set_homie_list()
        self.set_prev_homie("Nothing", "yet :(")

    def sort_homie_pics(self, homie: str) -> list[Path]:
        os.chdir(os.path.join(self.pics_directory, homie))
        sorted_list = sorted(Path(".").iterdir(),
                             key=lambda f: f.stat().st_ctime)
        os.chdir(self.base_directory)
        return [
            x for x in sorted_list if not x.parts[-1].startswith(".")
        ]

    def set_homie_list(self):
        self.homie_list = [
            homie
            for homie in os.listdir(self.pics_directory)
            if not (
                homie.startswith(".")
                or homie == "amogus"
                or homie == "hbk"
                or homie == "haram"
            )
        ]
        self.homie_pics_list = {
            homie: self.sort_homie_pics(homie)
            for homie in self.homie_list}

    def set_prev_homie(self, homie: str, j: int | str):
        self.prev_homie = f"{homie} {j}"

    async def get_stats(self, ctx: commands.Context):
        homies = [
            (homie, len(self.homie_pics_list[homie]))
            for homie in self.homie_list
        ]
        msg = "```\n"
        for homie in sorted(homies, key=lambda d: d[1], reverse=True):
            msg += f"{homie[0]} {homie[1]}\n"
        msg += "```"
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
        if name not in self.homie_list:
            await ctx.send("Invalid homie.")
            return
        if num != 0 and num >= len(self.homie_pics_list[name]):
            await ctx.send("Not a valid number")
            # TODO: Maybe ask if user wants to mod the number to return something in the future
            return
        await ctx.send(file=discord.File(os.path.join(self.pics_directory, name, self.homie_pics_list[name][num])), delete_after=5)

    async def get_homie_stat(self, ctx: commands.Context, name: str):
        if name not in self.homie_list:
            await ctx.send("Invalid homie.")
            return
        msg = f"```{name} {len(self.homie_pics_list[name])}```"
        await ctx.send(msg)

    async def get_prev_homie(self, ctx: commands.Context):
        await ctx.send(self.prev_homie, delete_after=5)

    @commands.command(
        name="homie",
        brief="Sends random homie pic",
        help="Send random homie pic. Use &homie [homie name] [opt]. Use &homie list for a list of names. Or &homie stats for stats on homie pics. Picks random homie if no arguement provided. Use opt to provide specific picture in database, or latest to get latest picture",
    )
    async def homies(self, ctx: commands.Context, homie="", opt=""):
        homie = homie.lower()
        match homie:
            case "stats":
                await self.get_stats(ctx)
                return
            case "aritzia":
                homie = "irtiza"
            case "list":
                await self.list(ctx)
                return
            case "prev":
                await self.get_prev_homie(ctx)
                return
            case _:
                pass

        if opt == "latest":
            opt = "-1"

        if opt == "stats":
            await self.get_homie_stat(ctx, homie)
            return

        homies = self.homie_list
        if not homie:
            i = random.randint(0, len(homies) - 1)
            homie = self.homie_list[i]
        else:
            if homie not in homies:
                await ctx.send("invalid homie")
                return
        if opt.isdigit() or opt == "-1":
            await self.get_num(ctx, homie, int(opt))
            return
        j = random.randint(0, len(self.homie_pics_list[homie]) - 1)
        homie_to_send = os.path.join(
            self.pics_directory, homie, self.homie_pics_list[homie][j])
        self.set_prev_homie(homie, j)
        await ctx.send(
            file=discord.File(homie_to_send), delete_after=5
        )

    async def list(self, ctx: commands.Context):
        homies = self.homie_list
        msg = "```\n"
        for homie in homies:
            msg += homie + "\n"
        msg += "```"
        await ctx.send(msg)

    @commands.command(
        name="homir",
        brief="Sends homie pic of mir",
        help="Easy mir spamming for your enjoyment :)",
    )
    async def homir(self, ctx: commands.Context, opt: str = ""):
        await self.homies(ctx, "mir", opt)

    @commands.command(
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

    @commands.command(
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

    @commands.command(
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
        self.set_homie_list()
        await ctx.send(f"folder {folder} added. use &addpic {folder} to add images.")

    @commands.command(
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
        if folder not in os.listdir(self.pics_directory):
            await ctx.send("folder does not exist.")
            return
        if len(os.listdir(os.path.join(self.pics_directory, folder))) == 0:
            shutil.rmtree(os.path.join(self.pics_directory, folder))
            self.set_homie_list()
            await ctx.send(f"folder {folder} removed.")
            return
        await ctx.send(f"folder {folder} not removed beacuse it's non-empty.")

    @commands.command(
        name="amogus",
        brief="Sends sus message from server.",
        help="Sends random sus message from server.",
    )
    async def sus(self, ctx: commands.Context):
        amogus_dir = os.path.join(self.pics_directory, "amogus")
        images = os.listdir(amogus_dir)
        i = random.randint(0, len(images) - 1)
        await ctx.send(file=discord.File(os.path.join(amogus_dir, images[i])))

    @commands.command(
        name="haram",
        brief="Sends haram accusation.",
        help="Sends random sus message from server.",
    )
    async def haram(self, ctx: commands.Context):
        haram_dir = os.path.join(self.pics_directory, "haram")
        images = os.listdir(haram_dir)
        i = random.randint(0, len(images) - 1)
        await ctx.send(file=discord.File(os.path.join(haram_dir, images[i])))

    @commands.command(
        aliases=["sad"],
        brief="Sends heartbroken quote/image.",
        help="Sends heartbroken quote/image.",
    )
    async def hbk(self, ctx: commands.Context):
        hbk_dir = os.path.join(self.pics_directory, "hbk")
        images = os.listdir(hbk_dir)
        i = random.randint(0, len(images) - 1)
        file = discord.File(os.path.join(hbk_dir, images[i]))
        text = images[i][:-3]
        if len(text) >= 40:
            await ctx.send(text, file=file)
        else:
            await ctx.send(file=file)


async def setup(bot: commands.Bot):
    await bot.add_cog(Pictures(bot))
