import discord
from discord.app_commands import command
from discord.ext import commands
from cogs.utils import UserBanned

import os
import random
import requests
import shutil
import string
from pathlib import Path
import boto3
import io

import typing
import sys
import traceback


class Pictures(commands.Cog):
    """All your pic related commands lie here."""
    


    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.base_directory = os.path.abspath(os.curdir)
        self.pics_directory = os.path.abspath(os.path.join(os.curdir, "pics"))
        self.set_prev_homie("Nothing", "yet :(")
        self.s3 = boto3.client('s3')
        self.bucket = "kanyeweastbotpics"
        self.set_homie_list()

    ##################################################################################################
    ####################################### COG ERROR HANDLER ########################################
    ##################################################################################################

    async def cog_command_error(self, ctx, error: commands.CommandError):
        if hasattr(ctx.command, "on_error"):
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
        if ctx.author.id in dev.banned_set:
            raise UserBanned(ctx.message.author)
        return True

    ##################################################################################################
    ##################################################################################################
    ##################################################################################################

    def sort_homie_pics(self, homie: str, update: str = "") -> list[str | None]:
        result = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=f'pics/{homie}/')
        mtime_sorted_list = sorted(result.get('Contents'), key=lambda x: x['LastModified'])
        keys_list = [ o.get('Key') for o in mtime_sorted_list ]
        if update:
            self.homie_pics_list[homie] = keys_list
        return keys_list

    def set_homie_list(self):
        result = self.s3.list_objects_v2(Bucket=self.bucket, Prefix='pics/', Delimiter='/')
        homies = {o.get('Prefix').split('/')[1] for o in result.get('CommonPrefixes')}
        self.homie_list = [
            homie
            for homie in homies
            if not (
                homie.startswith(".")
                or homie == "amogus"
                or homie == "sad"
                or homie == "haram"
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
        try:
            url = self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket':self.bucket, 'Key': self.homie_pics_list[name][num]},
                ExpiresIn=60
            )
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

    @commands.command(
        name="homie",
        brief="Sends random homie pic",
        help="Send random homie pic. Use &homie [homie name] [opt]. Use &homie list for a list of names. Or &homie stats for stats on homie pics. Picks random homie if no argument provided. Use opt to provide specific picture in database, or latest to get latest picture",
    )
    async def homies(self, ctx: commands.Context, homie="", opt=""):
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
            case _:
                pass

        match opt:
            case "latest":
                opt = "-1"

            case "stats":
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
        try:
            if opt:
                await self.get_num(ctx, homie, int(opt))
                return
        except ValueError as e:
            print(e)
        j = random.randint(0, len(self.homie_pics_list[homie]) - 1)
        self.set_prev_homie(homie, j)
        await self.get_num(ctx, homie, j)

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
            if name not in os.listdir(self.pics_directory):
                await ctx.send(
                    f"folder {name} does not exist. use &addfolder to create."
                )
            else:
                for attachment in ctx.message.attachments:
                    await self.save_pic(name, attachment)
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
        result = self.s3.list_objects_v2(Bucket=self.bucket, Prefix='pics/', Delimiter='/')
        subdirs = {o.get('Prefix').split('/')[1] for o in result.get('CommonPrefixes')}
        if folder in subdirs:
            await ctx.send("folder already exists.")
            return
        self.s3.put_object(Bucket=self.bucket, Key=f'pics/{folder}/')
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
        result = self.s3.list_objects_v2(Bucket=self.bucket, Prefix='pics/', Delimiter='/')
        subdirs = {o.get('Prefix').split('/')[1] for o in result.get('CommonPrefixes')}
        if folder not in subdirs:
            await ctx.send("folder does not exist.")
            return
        if len(self.sort_homie_pics(folder)) == 1:
            self.s3.delete_object(Bucket=self.bucket, Key=f'pics/{folder}/')
        await ctx.send(f"folder {folder} not removed beacuse it's non-empty.")

    @commands.command(
        name="amogus",
        brief="Sends sus message from server.",
        help="Sends random sus message from server.",
    )
    async def sus(self, ctx: commands.Context):
        images = self.sort_homie_pics("amogus")
        i = random.randint(0, len(images) - 1)
        url = self.s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': self.bucket, 'Key': images[i]},
            ExpiresIn=60
        )       
        await ctx.send(url)

    @commands.command(
        name="haram",
        brief="Sends haram accusation.",
        help="Sends random sus message from server.",
    )
    async def haram(self, ctx: commands.Context):
        images = self.sort_homie_pics("haram")
        i = random.randint(0, len(images) - 1)
        url = self.s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': self.bucket, 'Key': images[i]},
            ExpiresIn=60
        )       
        await ctx.send(url)

    @commands.command(
        name="",
        brief="Sends heartbroken quote/image.",
        help="Sends heartbroken quote/image.",
    )
    async def sad(self, ctx: commands.Context):
        images = self.sort_homie_pics("sad")
        i = random.randint(0, len(images) - 1)
        url = self.s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': self.bucket, 'Key': images[i]},
            ExpiresIn=60
        )
        file = discord.File(io.BytesIO(requests.get(url).content), filename="image.png")
        text = images[i][:-3]
        msg = ""
        if len(text) >= 40:
            msg = text.split("/")[-1]
        await ctx.send(msg if msg else None, file=file)

    async def save_pic(self, name: str, attachment: discord.Attachment):
        self.s3.upload_fileobj(io.BytesIO(await attachment.read()), self.bucket, f"pics/{name}/{attachment.filename}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Pictures(bot))
