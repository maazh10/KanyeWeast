import discord
from discord.ext import commands
import json
from random import randint
import asyncio
from time import sleep
import json

from cogs.utils import is_dev, get_color

with open('secrets.json') as f:
  keys = json.load(f)

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

bot: commands.Bot = commands.Bot(command_prefix='&', help_command = help_command, intents=discord.Intents.all())

@bot.command(name="play",
brief="Play donda chants",
help="Plays donda chants in the voice channel user is currently in.")
async def play(ctx: commands.Context):
    voice = ctx.author.voice
    if voice:
      voice_channel = voice.channel
      vc = await voice_channel.connect()
      vc.play(discord.FFmpegPCMAudio("play.mp3"))
      song_info = get_song_info("Donda Chant")
      embed = discord.Embed(
        title=song_info["name"], 
        url=song_info["url"], 
        description=song_info["lyrics"],
        color=song_info["color"])
      embed.set_thumbnail(url=song_info["thumbnail"])
      await ctx.send(embed=embed)
      while vc.is_playing():
          sleep(.1)
      await vc.disconnect()
    else:
      await ctx.send("You are not in a voice channel pleb.")        


@bot.event
async def on_message(message: discord.Message):
  await bot.process_commands(message)
  if message.author.id == bot.user.id:
    return
  res = ["what", "wat", "wht", "wot", "whot", "waht"]
  if not await is_dev(message.author) and message.content.lower() in res:
    await message.reply('smb')
  if message.author.id == 630492967018430489 and '<:lemean:903117276587376710>' in message.content:
    await message.reply('<:lemean:903117276587376710>')

bot.sniped_messages = {}
@bot.event
async def on_message_delete(message):
    if message.author == bot.user:
        return
    if message.attachments:
        bob = message.attachments[0]
        bot.sniped_messages[message.guild.id] = (bob.proxy_url, message.content, message.author, message.channel.name, message.created_at)
    else:
        bot.sniped_messages[message.guild.id] = (message.content,message.author, message.channel.name, message.created_at)

@bot.command(name="snipe",
brief="Snipes last deleted message in channel.",
help="Retrieves and sends the most recently deleted message in the server.")
async def snipe(ctx: commands.Context):
  try:
      bob_proxy_url, contents,author, channel_name, time = bot.sniped_messages[ctx.guild.id]
  except:
      try:
          contents,author, channel_name, time = bot.sniped_messages[ctx.guild.id]
      except:
          await ctx.channel.send("Couldn't find a message to snipe!")
          return
  try:
      pfp_url = author.avatar.url
      embed = discord.Embed(description=contents , color=await get_color(pfp_url), timestamp=time)
      embed.set_image(url=bob_proxy_url)
      embed.set_author(name=f"{author.name}#{author.discriminator} me", icon_url=pfp_url)
      embed.set_footer(text=f"Deleted in : #{channel_name}")
      await ctx.channel.send(embed=embed)
  except:
      pfp_url = author.avatar.url
      embed = discord.Embed(description=contents , color=await get_color(pfp_url), timestamp=time)
      embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=pfp_url)
      embed.set_footer(text=f"Deleted in : #{channel_name}")
      await ctx.channel.send(embed=embed)

async def load_cogs():
  """Loads cogs for bot"""
  cog_list = ['cogs.dev',
              'cogs.pics',
              'cogs.misc',
              'cogs.lyrics',
              'cogs.users'
              ]
  for cog in cog_list:
    await bot.load_extension(cog)

async def main():
  await load_cogs()
  await bot.start(keys['TOKEN'])

asyncio.run(main())
