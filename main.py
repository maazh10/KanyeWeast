from logging.config import IDENTIFIER
import discord
from discord.ext import commands
import os
import requests
import json
import random
from random import randint
import asyncio
import lyricsgenius
from colorthief import ColorThief
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from time import sleep
import string
import shutil
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import unicodedata
import pprint
import subprocess

with open('secrets.json') as f:
  keys = json.load(f)

def show_html(URL_input):
       html = Request(URL_input, headers={'User-Agent':'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25'})
       return(urlopen(html).read())

def donda_date():
    donda = BeautifulSoup(show_html('https://music.apple.com/us/album/donda/1583449420'), 'html.parser')
    date = donda.find("div", "product-meta typography-callout-emphasized")
    date = (date.text)
    date = (date.split("·"))
    for i in range(len(date)):
        date[i] = date[i].strip()
    return date

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

bot = commands.Bot(command_prefix='&', help_command = help_command, intents=discord.Intents.all())

@bot.command(name="morning",
brief="Kanye says good morning",
help="Are you dumb what is there to understand")
async def morning(ctx: commands.Context):
  embed = discord.Embed()
  embed.set_image(url="https://tenor.com/view/alarm-wake-up-tired-so-gif-24728280.gif")
  await ctx.send(embed=embed)

@bot.command(name="annoy", 
brief="Annoys mentioned user", 
help="Pings mentioned user the number of times specified")
async def annoy(ctx: commands.Context, user = None, num_str = None, opt_str = None):
  invalid_num = False
  in_range = True
  invalid_user = user[0] != "<"
  if num_str != None:
    invalid_num = not num_str.isdigit()
    if (not invalid_num):
      num = int(num_str)
      if(num > 69 or num < 0):
        in_range = False
  else:
    num = 1

  flag = False
  if user[0] == "<":
    print(user[2:-1])
    pinged = await bot.fetch_user(user[2:-1])
    flag = True

  if invalid_user or invalid_num or not in_range:
    await ctx.send("Specified number of times is too annoying or invalid or invalid user <:Pepepunch:794437891648520224>")
    num = 5
    user = await bot.fetch_user(ctx.author.id)

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

@bot.command(name="roast",
brief="Roast user",
help="Roasts the author or mentioned user.")
async def roast(ctx: commands.Context, user=None):
  with open("roasts.txt", "r") as f:
    lines = f.readlines()
    i = randint(0,len(lines))
    if user == None:
      await ctx.send(ctx.author.mention + ". " + lines[i])
    else:
      await ctx.send(user + ". " + lines[i])
 

@bot.command(aliases=["penis", "dick", "dagger", "glizzy", "ydd", "cock", "schlong"],
brief="Shows your pp.",
help="Shows your pp.")
async def pp(ctx: commands.Context, user=""):
  if user == "":
    user = ctx.message.author.name
    if ctx.message.author.id == int(keys['ID_STARBOY']) or ctx.message.author.id == int(keys['ID_BENNY']):
      length = 30
    else:
      length = randint(0, 30)
  else:
    user = user.replace("<", "")
    user = user.replace(">", "")
    id = user.replace("@", "")
    mem = await bot.fetch_user(id)
    if is_dev(mem): 
      length = 30
    else:
      length = randint(0, 30)
    user = mem.name
  
  penis = f"**{user}'s penis:**\n8"
  for i in range(length):
    penis += "="
  penis += "D\n"
  await ctx.send(penis)

@bot.event
async def on_message(message):
  await bot.process_commands(message)
  if message.author.id == bot.user.id:
    return
  res = ["what", "wat", "wht", "wot", "whot", "waht"]
  if message.author.id != 471459486125522946 and message.author.id != 687411480009637925 and message.content.lower() in res:
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
      embed = discord.Embed(description=contents , color=get_color(pfp_url), timestamp=time)
      embed.set_image(url=bob_proxy_url)
      embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=pfp_url)
      embed.set_footer(text=f"Deleted in : #{channel_name}")
      await ctx.channel.send(embed=embed)
  except:
      pfp_url = author.avatar.url
      embed = discord.Embed(description=contents , color=get_color(pfp_url), timestamp=time)
      embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=pfp_url)
      embed.set_footer(text=f"Deleted in : #{channel_name}")
      await ctx.channel.send(embed=embed)

async def load_cogs():
  """Loads cogs for bot"""
  cog_list = ['cogs.dev',
              'cogs.pics',
              'cogs.misc',
              'cogs.lyrics'
              ]
  for cog in cog_list:
    await bot.load_extension(cog)

async def main():
  await load_cogs()
  await bot.start(keys['TOKEN'])

asyncio.run(main())
