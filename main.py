import discord
from discord.ext import commands
import json
import asyncio
from random import randint

from cogs.utils import get_color

with open("secrets.json") as f:
    keys = json.load(f)

help_command = commands.DefaultHelpCommand(no_category="Commands")

owners = {int(keys["ID_BENNY"]), int(keys["ID_STARBOY"])}
# bot: commands.Bot = commands.Bot(
#     command_prefix="&",
#     help_command=help_command,
#     owner_ids=owners,
#     intents=discord.Intents.all(),
#     case_insensitive=True,
# )


class Bot_With_Sniped_Messages(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sniped_messages = {}


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
    if bot.user == None:
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


bot.sniped_messages = {}


@bot.event
async def on_message_delete(message):
    color = get_color(message.author.avatar.url)
    if message.attachments:
        bob = message.attachments[0]
        bot.sniped_messages[message.guild.id] = (
            bob.proxy_url,
            message.content,
            message.author,
            message.channel.name,
            message.created_at,
            color,
        )
    else:
        bot.sniped_messages[message.guild.id] = (
            message.content,
            message.author,
            message.channel.name,
            message.created_at,
            color,
        )


@bot.command(
    name="snipe",
    brief="Snipes last deleted message in channel.",
    help="Retrieves and sends the most recently deleted message in the server.",
)
async def snipe(ctx: commands.Context):
    bob_proxy_url = None
    if not ctx.guild:
        await ctx.channel.send("This command can only be used in a server!")
        return
    try:
        (contents, author, channel_name, time, color) = bot.sniped_messages[
            ctx.guild.id
        ][-5:]
        if len(bot.sniped_messages[ctx.guild.id]) == 6:
            bob_proxy_url = bot.sniped_messages[ctx.guild.id][0]
    except:
        await ctx.channel.send("Couldn't find a message to snipe!")
        return
    pfp_url = author.avatar.url
    embed = discord.Embed(description=contents, color=color, timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=pfp_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")
    if bob_proxy_url is not None:
        embed.set_image(url=bob_proxy_url)
    await ctx.channel.send(embed=embed)


async def load_cogs():
    """Loads cogs for bot"""
    cog_list = ["cogs.dev", "cogs.pics", "cogs.misc", "cogs.music", "cogs.users"]
    for cog in cog_list:
        await bot.load_extension(cog)


async def load_cogs_wrapper():
    await load_cogs()


asyncio.run(load_cogs_wrapper())
bot.run(keys["TOKEN"])
