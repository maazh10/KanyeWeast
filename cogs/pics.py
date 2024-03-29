import io
import json
import logging
from datetime import datetime, timezone
from random import choice, randint
from fuzzywuzzy import process

import boto3
import discord
import requests
from discord.ext import commands

import cogs.CustomPaginator as BennysCustomPaginator
from cogs.dev import DevelopersOnly
from cogs.utils import UserBanned


class Pictures(commands.Cog):
    """All your pic related commands lie here."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.set_prev_homie("Nothing", "yet :(")
        self.latest_date: datetime = datetime.min.replace(tzinfo=timezone.utc)
        self.latest_pic: str = ""
        self.s3 = boto3.client("s3")
        self.bucket = "discordbotpics"
        self.set_homie_list()
        with open("secrets.json") as f:
            self.keys = json.load(f)

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
    ##############################
    ##############################

    def sort_homie_pics(self, homie: str, update: str = "") -> list[str | None]:
        result = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=f"pics/{homie}/")
        mtime_sorted_list = sorted(
            result.get("Contents"), key=lambda x: x["LastModified"]
        )
        if mtime_sorted_list[-1].get("LastModified") > self.latest_date:
            self.latest_pic = mtime_sorted_list[-1].get("Key", "")
            self.latest_date = mtime_sorted_list[-1].get("LastModified")
        keys_list = [o.get("Key") for o in mtime_sorted_list]
        if update:
            self.homie_pics_list[homie] = keys_list
        return keys_list

    async def save_pic(self, name: str, attachment: discord.Attachment):
        self.s3.upload_fileobj(
            io.BytesIO(await attachment.read()),
            self.bucket,
            f"pics/{name}/{attachment.filename}",
        )

    def set_homie_list(self):
        result = self.s3.list_objects_v2(
            Bucket=self.bucket, Prefix="pics/", Delimiter="/"
        )
        homies = {o.get("Prefix").split("/")[1] for o in result.get("CommonPrefixes")}
        self.homie_list = [
            homie
            for homie in homies
            if not (
                homie.startswith(".")
                or homie == "amogus"
                or homie == "sad"
                or homie == "haram"
                or homie == "album"
            )
        ]
        self.homie_pics_list = {
            homie: self.sort_homie_pics(homie) for homie in self.homie_list
        }

    def set_prev_homie(self, homie: str, j: int | str):
        self.prev_homie = f"{homie} {j}"

    async def get_stats(self, ctx: commands.Context):
        homies = [
            (homie, len(self.homie_pics_list[homie])) for homie in self.homie_list
        ]
        msg = "```\n"
        for homie in sorted(homies, key=lambda d: d[1], reverse=True):
            msg += f"{homie[0]: <10}{homie[1]: >4}\n"
        msg += "```"
        await ctx.send(msg)

    async def get_num(self, ctx: commands.Context, name: str = "", num: int = -1):
        if name == "":
            await ctx.send("Must provide name.")
            return
        if name not in self.homie_list:
            await ctx.send("Invalid homie.")
            return
        logging.getLogger("discord").info(f"Getting {name} {num}")
        try:
            url = self.s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": self.homie_pics_list[name][num]},
                ExpiresIn=60,
            )
            await ctx.send(f"{name.capitalize()} #{num}", delete_after=5)
            await ctx.send(
                url,
                delete_after=5,
            )
        except IndexError:
            if num == len(self.homie_pics_list[name]):
                await ctx.send("It's zero-indexed bozo")
                return
            await ctx.send("Not a valid number for this homie")
            # TODO: Maybe ask if user wants to mod the number to return something in the future
            return

    async def get_homie_stat(self, ctx: commands.Context, name: str):
        if name not in self.homie_list:
            await ctx.send("Invalid homie.")
            return
        msg = f"```{name: <10}{len(self.homie_pics_list[name]): >4}```"
        await ctx.send(msg)

    async def get_prev_homie(self, ctx: commands.Context):
        await ctx.send(self.prev_homie, delete_after=5)
        prev_homie = self.prev_homie.split(" ")
        await ctx.invoke(self.homies, homie=prev_homie[0], opt=prev_homie[1])

    async def get_latest_homie_pic(self, ctx: commands.Context):
        if self.latest_pic == "":
            await ctx.send("No new homie pics added yet :(")
            return
        url = self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": self.latest_pic},
            ExpiresIn=60,
        )
        await ctx.send(
            url,
            delete_after=5,
        )

    @commands.command(
        name="homie",
        brief="Sends random homie pic",
        help="Send random homie pic. Use &homie [homie name] [opt]. Use &homie list for a list of names. Or &homie stats for stats on homie pics. Picks random homie if no argument provided. Use opt to provide specific picture in database, or latest to get latest picture",
    )
    async def homies(self, ctx: commands.Context, homie="", opt=""):
        if isinstance(ctx.message.channel, discord.DMChannel):
            if not (
                await self.bot.is_owner(ctx.message.author)
                or ctx.message.author.id == int(self.keys["ID_LUCE"])
            ):
                await ctx.send("You can't use this command in DMs")
                return

        homie = homie.lower()
        match homie:
            case "stats":
                await self.get_stats(ctx)
                return
            case "aritzia":
                homie = "irtiza"
            case "luce":
                await ctx.send("too cool for pics :)")
                return
            case "list":
                await self.list(ctx)
                return
            case "prev":
                await self.get_prev_homie(ctx)
                return
            case "latest":
                await self.get_latest_homie_pic(ctx)
                return
            case _:
                pass

        match opt:
            case "latest":
                opt = "-1"
            case "stats":
                await self.get_homie_stat(ctx, homie)
                return
            case "gallery":
                await self.get_gallery(ctx, homie)
                return

        homies = self.homie_list
        if not homie:
            homie = choice(self.homie_list)
        else:
            if homie not in homies:
                closest_match, _ = process.extractOne(homie, homies)
                homie = closest_match
        try:
            if opt:
                await self.get_num(ctx, homie, int(opt))
                return
        except ValueError as e:
            print(e)
        j = randint(0, len(self.homie_pics_list[homie]) - 1)
        self.set_prev_homie(homie, j)
        await self.get_num(ctx, homie, j)

    async def list(self, ctx: commands.Context):
        homies = self.homie_list
        msg = "```\n"
        for homie in homies:
            msg += homie + "\n"
        msg += "```"
        await ctx.send(msg)

    async def get_gallery(self, ctx: commands.Context, homie: str = ""):
        images = self.homie_pics_list[homie]
        embeds = []
        for i in range(len(images) - 1, -1, -1):
            embed = discord.Embed(
                title=f"{homie.capitalize()}'s Gallery 💞",
                color=discord.Color(randint(0, 0xFFFFFF)),
            )
            key = self.homie_pics_list[homie][i]
            embeds.append((embed, key))
        await BennysCustomPaginator.Simple().start(ctx, pages=embeds)

    @commands.command(
        name="homir",
        brief="Sends homie pic of mir",
        help="Easy mir spamming for your enjoyment :)",
    )
    async def homir(self, ctx: commands.Context, opt: str = ""):
        await self.homies(ctx, "mir", opt)

    @commands.command(
        name="homz",
        brief="Sends homie pic of maaz",
        help="Easy maaz spamming for your enjoyment :)",
    )
    async def homz(self, ctx: commands.Context, opt: str = ""):
        await self.homies(ctx, "maaz", opt)

    @commands.command(
        name="homo",
        brief="Sends homie pic of null",
        help="Easy null spamming for your enjoyment :)",
    )
    async def homo(self, ctx: commands.Context, opt: str = ""):
        await self.homies(ctx, "mo", opt)

    ##################################################################################################
    ###################################### CUSTOM STR CONVERTER ######################################
    ##################################################################################################

    class BennysStrConverter(commands.Converter):
        async def convert(self, ctx, argument) -> str:
            return str(argument).lower()

    ##################################################################################################

    @commands.command(
        name="addpic",
        brief="Adds a new image to specified folder(s).",
        help="Add a new image by adding the image as an attachment and specifying a folder location(s) (homie name) or amogus for sus quotes. &addpic {foldername} {foldername} ... {foldername}. Use &homie list to get valid homies.",
    )
    async def addpic(
        self,
        ctx: commands.Context,
        folders: commands.Greedy[BennysStrConverter] = commands.parameter(
            description=": Name of homie to add pic to."
        ),
    ):
        if not folders:
            await ctx.send("please specify folder(s).")
            return
        if len(ctx.message.attachments) == 0:
            await ctx.send("attach an image to be added.")
            return
        for name in folders:
            result = self.s3.list_objects_v2(
                Bucket=self.bucket, Prefix="pics/", Delimiter="/"
            )
            subdirs = {
                o.get("Prefix").split("/")[1] for o in result.get("CommonPrefixes")
            }
            if name not in subdirs:
                await ctx.send(
                    f"folder {name} does not exist. use &addfolder to create."
                )
            else:
                for attachment in ctx.message.attachments:
                    await self.save_pic(name, attachment)
                length = len(ctx.message.attachments)
                await ctx.send(
                    f"{str(length) + ' ' if length > 1 else ''}image{'s' * (length > 1)} added to {name}."
                )
                self.sort_homie_pics(name, update="update")

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
        result = self.s3.list_objects_v2(
            Bucket=self.bucket, Prefix="pics/", Delimiter="/"
        )
        subdirs = {o.get("Prefix").split("/")[1] for o in result.get("CommonPrefixes")}
        if folder in subdirs:
            await ctx.send("folder already exists.")
            return
        self.s3.put_object(Bucket=self.bucket, Key=f"pics/{folder}/")
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
        result = self.s3.list_objects_v2(
            Bucket=self.bucket, Prefix="pics/", Delimiter="/"
        )
        subdirs = {o.get("Prefix").split("/")[1] for o in result.get("CommonPrefixes")}
        if folder not in subdirs:
            await ctx.send("folder does not exist.")
            return
        if len(self.sort_homie_pics(folder)) == 1:
            self.s3.delete_object(Bucket=self.bucket, Key=f"pics/{folder}/")
        await ctx.send(f"folder {folder} not removed beacuse it's non-empty.")

    async def get_presigned_url(self, folder: str) -> str:
        images = self.sort_homie_pics(folder)
        return self.s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.bucket, "Key": choice(images)},
            ExpiresIn=60,
        )

    @commands.is_owner()
    @commands.command(
        name="update",
        brief="Updates homie pics list.",
        help="Updates homie pics list.",
    )
    async def update(self, ctx: commands.Context, homie: str = ""):
        if homie:
            if homie not in self.homie_list:
                await ctx.send("Invalid homie.")
                return
            self.sort_homie_pics(homie, update="update")
            await ctx.send(f"{homie} updated.")
        else:
            await ctx.send("homie list updated.")
            self.set_homie_list()

    @commands.command(
        name="amogus",
        brief="Sends sus message from server.",
        help="Sends random sus message from server.",
    )
    async def sus(self, ctx: commands.Context):
        url = await self.get_presigned_url("amogus")
        await ctx.send(url)

    @commands.command(
        name="haram",
        brief="Sends haram accusation.",
        help="Sends random sus message from server.",
    )
    async def haram(self, ctx: commands.Context):
        url = await self.get_presigned_url("haram")
        await ctx.send(url)

    @commands.command(
        name="",
        brief="Sends heartbroken quote/image.",
        help="Sends heartbroken quote/image.",
    )
    async def sad(self, ctx: commands.Context):
        images = self.sort_homie_pics("sad")
        i = randint(0, len(images) - 1)
        url = self.s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.bucket, "Key": images[i]},
            ExpiresIn=60,
        )
        file = discord.File(io.BytesIO(requests.get(url).content), filename="image.png")
        text = images[i][:-3]
        msg = ""
        if len(text) >= 40:
            msg = text.split("/")[-1]
        await ctx.send(msg if msg else None, file=file)

    @commands.command(
        name="",
        brief="Sends a homie pic as an album art.",
        help="Sends an edited homie pic as an album art.",
    )
    async def album(self, ctx: commands.Context, index: int = -1):
        images = self.sort_homie_pics("album")
        key = images[index] if index != -1 else choice(images)
        try:
            url = self.s3.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": self.bucket, "Key": key},
                ExpiresIn=60,
            )
            await ctx.send(url)
        except IndexError:
            await ctx.send(
                f"index out of range. Choose a number between 0 and {len(images) - 1}."
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Pictures(bot))
