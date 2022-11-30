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
bot: commands.Bot = commands.Bot(
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
    res = ["what", "wat", "wht", "wot", "whot", "waht"]
    if not await bot.is_owner(message.author) and message.content.lower() in res:
        await message.reply("smb")
    if (
        message.author.id == 630492967018430489
    ):
        if ("<:lemean:903117276587376710>" in message.content):
            await message.reply("<:lemean:903117276587376710>")
        if message.channel.id == 892504507106361394:
            if (randint(0, 1000) % 7 == 0):
                await message.reply(file=discord.File("irtiza's_L.png"))
            if (randint(0, 1000) % 7 == 4):
                await message.reply(file=discord.File("irtiza's_other_L.png"))


bot.sniped_messages = {}


@bot.event
async def on_message_delete(message):
    if message.attachments:
        bob = message.attachments[0]
        bot.sniped_messages[message.guild.id] = (
            bob.proxy_url,
            message.content,
            message.author,
            message.channel.name,
            message.created_at,
        )
    else:
        bot.sniped_messages[message.guild.id] = (
            message.content,
            message.author,
            message.channel.name,
            message.created_at,
        )


@bot.command(
    name="snipe",
    brief="Snipes last deleted message in channel.",
    help="Retrieves and sends the most recently deleted message in the server.",
)
async def snipe(ctx: commands.Context):
    try:
        bob_proxy_url, contents, author, channel_name, time = bot.sniped_messages[
            ctx.guild.id
        ]
    except:
        try:
            contents, author, channel_name, time = bot.sniped_messages[ctx.guild.id]
        except:
            await ctx.channel.send("Couldn't find a message to snipe!")
            return
    try:
        pfp_url = author.avatar.url
        embed = discord.Embed(
            description=contents, color=await get_color(pfp_url), timestamp=time
        )
        embed.set_image(url=bob_proxy_url)
        embed.set_author(
            name=f"{author.name}#{author.discriminator}", icon_url=pfp_url)
        embed.set_footer(text=f"Deleted in : #{channel_name}")
        await ctx.channel.send(embed=embed)
    except:
        pfp_url = author.avatar.url
        embed = discord.Embed(
            description=contents, color=await get_color(pfp_url), timestamp=time
        )
        embed.set_author(
            name=f"{author.name}#{author.discriminator}", icon_url=pfp_url)
        embed.set_footer(text=f"Deleted in : #{channel_name}")
        await ctx.channel.send(embed=embed)


async def load_cogs():
    """Loads cogs for bot"""
    cog_list = ["cogs.dev", "cogs.pics",
                "cogs.misc", "cogs.music", "cogs.users"]
    for cog in cog_list:
        await bot.load_extension(cog)


async def main():
    await load_cogs()
    await bot.start(keys["TOKEN"])


asyncio.run(main())
