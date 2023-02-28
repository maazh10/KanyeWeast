import asyncio
import json
from operator import le

import discord
from discord.ext import commands

from cogs.utils import get_color

with open("secrets.json") as f:
    keys = json.load(f)

help_command = commands.DefaultHelpCommand(no_category="Commands")

owners = {int(keys["ID_BENNY"]), int(keys["ID_STARBOY"])}


class Bot_With_Sniped_Messages(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sniped_messages = {}
        self.sniped_len = 5


bot = Bot_With_Sniped_Messages(
    command_prefix="&",
    help_command=help_command,
    owner_ids=owners,
    intents=discord.Intents.all(),
    case_insensitive=True,
)


@bot.event
async def on_message(message: discord.Message):
    await bot.process_commands(message)
    if bot.user is not None:
        return
    if message.author.id == bot.user.id:
        return
    what_responses = {"what", "wat", "wht", "wot", "whot", "waht"}
    if (
        not (
            await bot.is_owner(message.author)
            or message.author.id == int(keys["ID_TINA"])
        )
        and message.content.lower() in what_responses
    ):
        await message.reply("smb")
    if message.author.id == 630492967018430489:
        if "<:lemean:903117276587376710>" in message.content:
            await message.reply("<:lemean:903117276587376710>")


@bot.event
async def on_message_delete(message):
    if bot.sniped_messages.get(message.guild.id) is None:
        bot.sniped_messages[message.guild.id] = []
    color = get_color(message.author.avatar.url)
    sniped_content = (message.content, message.author, message.channel.name, message.created_at, color)
    if message.attachments:
       sniped_content = (message.attachments[0].proxy_url,) + sniped_content
    if len(bot.sniped_messages[message.guild.id]) == bot.sniped_len:
        bot.sniped_messages[message.guild.id].pop(0)
    bot.sniped_messages[message.guild.id].append(sniped_content)

async def build_sniped_message(ctx: commands.Context, sniped_content: tuple):
    bob_proxy_url = None
    if len(sniped_content) == 6:
        bob_proxy_url = sniped_content[0]
    (contents, author, channel_name, time, color) = sniped_content[-5:]
    pfp_url = author.avatar.url
    embed = discord.Embed(description=contents, color=color, timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=pfp_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")
    if bob_proxy_url is not None:
        embed.set_image(url=bob_proxy_url)
    await ctx.channel.send(embed=embed)

@commands.is_owner()
@bot.command(
    name="setsnipenum",
    brief="Sets the number of snipes to save",
    help="Sets the number of snipes to save"
)
async def setsnipelen(ctx: commands.Context, len: commands.Range[int, 0, 20] = 5):
    bot.sniped_len = len
    await ctx.send(f"Snipe number set to {len}")

def ordinal(x):
            return [
                "1st",
                "2nd",
                "3rd",
                "4th",
                "5th",][abs(x) - 1]

@bot.command(
    name="snipe",
    brief="Snipes last deleted message in channel.",
    help="Retrieves and sends the most recently deleted message in the server.",
)
async def snipe(ctx: commands.Context, snipe_num: commands.Range[int, -bot.sniped_len, -1] = -1):
    if not ctx.guild:
        await ctx.channel.send("This command can only be used in a server!")
        return
    try:
        sniped_content = bot.sniped_messages[ctx.guild.id][snipe_num]
        await build_sniped_message(ctx, sniped_content)
    except IndexError:
        await ctx.channel.send(f"Couldn't find the {ordinal(snipe_num)} deleted message.")
        return
    except KeyError:
        await ctx.channel.send("Couldn't find a message to snipe!")
        return

@snipe.error
async def snipe_on_error(ctx: commands.Context, error):
    if isinstance(error, commands.BadArgument):
        await ctx.channel.send(f"Please enter a valid number between -{bot.sniped_len} and -1.")
        return
    raise error

async def load_cogs():
    """Loads cogs for bot"""
    cog_list = ["cogs.dev", "cogs.pics", "cogs.misc", "cogs.music", "cogs.users"]
    for cog in cog_list:
        await bot.load_extension(cog)


asyncio.run(load_cogs())
bot.run(keys["TOKEN"])
