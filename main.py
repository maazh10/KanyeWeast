import discord
from discord.ext import commands
import os
import requests
import json
import re
import random
from random import randint
import asyncio
import lyricsgenius
from colorthief import ColorThief
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import datetime
import pickle
from database import db, valid_courses, TBD_DATE
from time import sleep
import string
import shutil
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

os.chdir('C:\\Users\\mhash\\Desktop\\KanyeWeast')
f = open('secrets.json')
keys = json.load(f)

def get_spotify_url(song_name: str):
  sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = keys['SPOTIFY_CLIENT_ID'] , client_secret = keys['SPOTIFY_CLIENT_SECRET']))
  results = sp.search(q = song_name, limit=1)
  return results['tracks']['items'][0]['external_urls']['spotify']

def search_for_water_type(test: str):
  pokemon = test.split("`")[1]
  pokemon = pokemon.replace("_", ".")
  file = open("water_pokemon.txt", "r")
  return_str = ""
  for line in file:
    if re.search(pokemon, line):
      return_str = return_str + line
  return return_str

def search_in_dex(pokemon: str):
  pokemon = pokemon.replace("\_", ".")
  print(pokemon)
  return_str = ""
  with open("national-dex.txt", "r") as dex:
    for line in dex:
      if re.search(f"\|{pokemon}\|", line):
        return_str = return_str + line.split("|")[1]
  print(return_str)
  return return_str
  # file = open("water_pokemon.txt", "r")
  # return_str = ""
  # for line in file:
  #   if re.search(pokemon, line):
  #     return_str = return_str + line
  # return return_str

def get_national_dex(pokemon: str):
  pokemon = pokemon.replace("\_", ".")
  return_str = ""
  with open("national-dex.txt", "r") as dex:
    for line in dex:
      if re.search(pokemon, line):
        return_str = line
        break
  n_and_name = return_str.split("|")
  return {"number":n_and_name[0][1:4], "name":n_and_name[1], "imageurl":n_and_name[2]}

def get_quote():
  response = requests.get("https://api.kanye.rest")
  json_data = json.loads(response.text)
  return json_data["quote"]

def get_lyric(k_or_w_or_d: str):
  if k_or_w_or_d == "k":
    all_albums = {
      0:["Lyrics_TheCollegeDropout_withList.json", "The College Dropout", 4331796],
      1:["Lyrics_808sHeartbreak_withList.json", "808s and Heartbreak", 12897227],
      2:["Lyrics_Graduation_withList.json", "Graduation", 10112126],
      3:["Lyrics_JESUSISKING_withList.json", "Jesus Is King", 402108],
      4:["Lyrics_KanyeWestPresentsGoodMusicCruelSummer_withList.json", "Good Music, Cruel Summer", 14803425],
      5:["Lyrics_KIDSSEEGHOSTS_withList.json", "KIDS SEE GHOSTS", 12890526],
      6:["Lyrics_LateRegistration_withList.json", "Late Registration", 1511179],
      7:["Lyrics_MyBeautifulDarkTwistedFantasy_withList.json", "My Beautiful Dark Twisted Fantasy", 15345470],
      8:["Lyrics_TheLifeofPablo_withList.json", "The Life of Pablo",  0xf48c54],
      9:["Lyrics_WatchtheThrone_withList.json", "Watch the Throne", 15238995],
      10:["Lyrics_ye_withList.json", "ye", 13092804],
      11:["Lyrics_Yeezus_withList.json", "Yeezus", 6955557],
      12:["Lyrics_Donda_withList.json", "Donda", 0x2596be]}
  elif k_or_w_or_d == "w":
    all_albums = {
    0:["Lyrics_AfterHours_withList.json", "After Hours", 2104082],
    1:["Lyrics_BeautyBehindtheMadness_withList.json", "Beauty Behind the Madness", 13026239],
    2:["Lyrics_EchoesofSilence_withList.json", "Echoes of Silence", 2300954],
    3:["Lyrics_HouseofBalloons_withList.json", "House of Balloons", 3289393],
    4:["Lyrics_KissLand_withList.json", "Kiss Land", 792342],
    5:["Lyrics_Starboy_withList.json", "Starboy", 13711403],
    6:["Lyrics_Thursday_withList.json", "Thursday", 15197149],
    7:["Lyrics_Trilogy_withList.json", "Trilogy", 460551],
    8:["Lyrics_DawnFM_withList.json", "Dawn FM", 3569036]}
  # if (album == ""):
  elif k_or_w_or_d == "d":
    all_albums = {
      0: ["Lyrics_CarePackage_withList.json", "Care Package", 460552],
      1: ["Lyrics_CertifiedLoverBoy_withList.json", "Certified Lover Boy", 12344040],
      2: ["Lyrics_HonestlyNevermind_withList.json", "Honestly Nevermind", 921616],
      3: ["Lyrics_ComebackSeason_withList.json", "Comeback Season", 12287806],
      4: ["Lyrics_DarkLaneDemoTapes_withList.json", "Dark Lane Demo Tapes", 1382408],
      5: ["Lyrics_IfYoureReadingThisItsTooLate_withList.json", "If You're Reading This It's Too Late", 14408925],
      6: ["Lyrics_MoreLife_withList.json", "More Life", 12686196],
      7: ["Lyrics_NothingWastheSame_withList.json", "Nothing Was The Same", 3707854],
      8: ["Lyrics_RoomforImprovement_withList.json", "Room For Improvement", 1710877],
      9: ["Lyrics_ScaryHours_withList.json", "Scary Hours", 2631720],
      10: ["Lyrics_SoFarGone_withList.json", "So Far Gone", 263172],
      11: ["Lyrics_ThankMeLater_withList.json", "Thank Me Later", 525573],
      12: ["Lyrics_TheBestintheWorldPack_withList.json", "The Best In The World Pack", 394758],
      13: ["Lyrics_Views_withList.json", "Views", 6056047],
      14: ["Lyrics_WhataTimeToBeAlive_withList.json", "What a Time To Be Alive", 12895432],
      15: ["Lyrics_Scorpion_withList.json", "Scorpion", 3355443],
      16: ["Lyrics_TakeCare_withList.json", "Take Care", 11769461]
    }
    
  albumnumber = randint(0, len(all_albums)-1)
  # print(f"albumnumber - {albumnumber}")
  file = open("lyrics/{0}/{1}".format(k_or_w_or_d, all_albums[albumnumber][0]))
  # else:
  #   for i in range(len(all_albums)):
  #     if album.lower() in all_albums[i][2].lower():
  #       file = open("{0}/{1}".format(k_or_w, all_albums[i][0]))
  #       albumnumber = i
  #       break
  data = json.load(file)
  songnumber = randint(0, len(data['tracks'])-1)
  # print(f"songnumber - {songnumber}")
  lyricnumber = randint(0, len(data['tracks'][songnumber]['song']['lyrics'])-1 )
  # print(f"lyricnumber - {lyricnumber}")
  return_dict = {"lyric":data['tracks'][songnumber]['song']['lyrics'][lyricnumber], "album_art":data['cover_art_url'], "album_name":data['name'],
  "song_name":data['tracks'][songnumber]['song']['title_with_featured'], "album_url":data['url'], "song_url":data['tracks'][songnumber]['song']['url'], "album_color":all_albums[albumnumber][-1]}
  file.close()
  return return_dict

def get_color(img_url):
    color_thief = ColorThief(requests.get(img_url, stream=True).raw)
    dominant_color = color_thief.get_color(quality=1)
    rgb2hex = lambda r,g,b: f"#{r:02x}{g:02x}{b:02x}"
    hexa = rgb2hex(dominant_color[0],dominant_color[1],dominant_color[2])
    hexa = hexa.replace("#","")
    return int(hexa, 16)

def clean_lyric_footer(lyric):
    i = lyric.find("Embed") - 1
    if i != -1:
      if lyric[i-2:i].isnumeric():
        lyric = lyric[:i-2]
      elif lyric[i-1:i].isnumeric():
        lyric = lyric[:i-1]
      elif lyric[i].isnumeric():
        lyric = lyric[:i]
    return lyric
    
def get_song_info(to_search):
    genius = lyricsgenius.Genius(keys['GENIUS_TOKEN'])
    song = genius.search_song(to_search);
    lyrics = clean_lyric_footer(song.lyrics)
    return {"name": song.full_title, "url": song.url, "lyrics": lyrics, "color": get_color(song.header_image_thumbnail_url),"thumbnail": song.header_image_thumbnail_url}

def check_if_caught(num, name):
  caught_list = "caught_pokemon.txt" if (name == "me") else "caught_pokemon_vivian.txt"
  caught = open("{}".format(caught_list), "r")
  for line in caught:
    if re.search(num, line):
      caught.close()
      return True
  caught.close()
  return False

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

def loadlist(filename):
  with open(filename, "rb") as file:
    pkl_list = pickle.load(file)
  return pkl_list

def dumplist(pkl_list: list, filename):
  with open(filename, "wb") as file:
    pickle.dump(pkl_list, file)

def sort_db():
  for course in db:
    data = db[course]
    sorted_values = sorted(data.values())
    sorted_db = {}

    for i in sorted_values:
      for k in data.keys():
          if data[k] == i and k not in sorted_db:
              sorted_db[k] = data[k]
              break
    db[course] = sorted_db

def parse_dt(dt):
  return {"year": dt.strftime("%Y"), "month": dt.strftime("%B"), "day": dt.strftime("%d"), "hour": dt.strftime("%I"), "min": dt.strftime("%M"), "ampm": dt.strftime("%p")}

def est_now():
  now = datetime.datetime.now()
  hour = (now.hour - 4) if ((now.hour - 4) >= 0) else 0
  return datetime.datetime(now.year, now.month, now.day, hour, now.minute)

def find_nearest_upcoming(dates):
  now = est_now()
  for event in sorted(dates):
    if event >= now:
      return event
  return None 

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

bot = commands.Bot(command_prefix='&', help_command = help_command, intents=discord.Intents.all())

########################################################################################################

# class Confirm(discord.ui.View):
#     def __init__(self):
#         super().__init__()
#         self.value = None

#     # When the confirm button is pressed, set the inner value to `True` and
#     # stop the View from listening to more input.
#     # We also send the user an ephemeral message that we're confirming their choice.
#     @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
#     async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
#         await interaction.response.send_message('Confirming', ephemeral=True)
#         self.value = True
#         self.stop()

#     # This one is similar to the confirmation button except sets the inner value to `False`
#     @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
#     async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
#         await interaction.response.send_message('Cancelling', ephemeral=True)
#         self.value = False
#         self.stop()

########################################################################################################

@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

@bot.command(
  name="hello",
  brief="Says hello",
  help="Says hello to whoever used the `hello` command"
  )
async def hello(ctx):
  if str(ctx.author.id) == keys['MY_ID'] or str(ctx.author.id) == keys['ID_STARBOY']:
    if ctx.message.content.endswith('son'):
        await ctx.send('Hello master!')
    else:
        await ctx.send('Hello ' + ctx.author.display_name + '!')
  else:
    if ctx.message.content.endswith('dad'):
      await ctx.send('Hello son!')
    else:
      await ctx.send('Hello '+ ctx.author.display_name + '!')

@bot.command(
  aliases=["donda?", "donda"],
  brief="Says whether Donda is out or not",
  help="Says whether Donda is out or not (long version)"
  )
async def rembr(ctx):
  await ctx.send('i rember <:3736_GalaxyBrainPepe:769650997681061950>')
  embed = discord.Embed()
  embed.description = '[Out 2021](https://music.apple.com/us/album/donda/1583449420)'
  await ctx.send(embed=embed)

@bot.command(name="quote",
  brief="Says a Kanye quote",
  help="Says a Kanye quote using a Kanye quote API"
  )
async def quote(ctx):
  embed = discord.Embed()
  embed.description='[{}](https://www.youtube.com/watch?v=dQw4w9WgXcQ)'.format(get_quote())
  await ctx.send(embed=embed)

@bot.command(name="spawn",
  brief="Says name of pokemon spawned from Mewbot",
  help="Gives the name and pokemondb entry of most recent spawned pokemon. Add caught to command to see most recent caught pokemon name and link")
async def spawn(ctx):
  prefix = "the pok"
  flag = False
  async for mesg in ctx.channel.history(limit=50):
    if mesg.author.id == 716390085896962058:
          if (mesg.content.lower().startswith(prefix)):
            pokemon1 = mesg.content.split()[-1]
            flag = True
            break
  if (flag):
    pokemon = get_national_dex(pokemon1)
    embed = discord.Embed(title=pokemon['name'], url="https://bulbapedia.bulbagarden.net/wiki/{}_(Pokémon)".format(pokemon['name']).replace(" ", "_"), description="#{0} - {1}".format(pokemon['number'], pokemon['name']))
    # if str(ctx.author.id) == os.getenv('MY_ID'):
    #   embed.add_field(name="Caught?", value = ( "Yes" if (check_if_caught(pokemon['number'], "me")) else "No"), inline=True)
    # elif str(ctx.author.id) == os.getenv('ID_VIVIAN'):
    #   embed.add_field(name="Caught?", value = ( "Yes" if (check_if_caught(pokemon['number'], "vivian")) else "No"), inline=True)
    #embed.add_field(name="Shiny?", value=pokemon["shiny"])
    embed.set_thumbnail(url=pokemon["imageurl"])
    await ctx.send(embed=embed)

@bot.command(name="fish",
  brief="Says the name of the pokemon spawned from mewbot fish",
  help="Says the name of the pokemon from most recent fish command from Mewbot")
async def fish(ctx):
  async for mesg in ctx.channel.history(limit=50):
    if mesg.author.id == 519850436899897346:
      e = mesg.embeds
      if len(e) != 0:
        e_dict = e[0].to_dict()
        if 'title' in e_dict:
          msg = mesg
          break
  embeds = msg.embeds
  embed_content_in_dict = embeds[0].to_dict()
  pokemon = search_for_water_type(embed_content_in_dict['title'])
  print(pokemon)
  await ctx.send(pokemon)

@bot.command(name="rick",
brief="Get Rick'd",
help="Are you dumb what is there to understand")
async def rick(ctx):
  embed = discord.Embed()
  embed.set_image(url="https://media1.tenor.com/images/3e30fa16b8a79b44185060d0df450009/tenor.gif?itemid=19920902")
  embed.description='Never gonna give you up'
  await ctx.send(embed=embed, delete_after=8)

@bot.command(name="bar",
brief="Says a Kanye lyric",
help="Says a random Kanye lyric from any of his albums")
async def bar(ctx):
  async with ctx.message.channel.typing():
    lyric = get_lyric("k")
    embed = discord.Embed(title=lyric["song_name"], url = lyric["song_url"], description=lyric["lyric"], color=(lyric["album_color"]) )
    embed.set_thumbnail(url=lyric["album_art"])
    embed.add_field(name="\u200B", value="[{0}]({1})".format(lyric["album_name"], lyric['album_url']), inline=False)
    embed.add_field(name="\u200B", value=":musical_note: [Spotify]({})".format(get_spotify_url(lyric["song_name"])), inline=False)
    await ctx.send(embed=embed)

@bot.command(name="weeknd",
brief="Says a lyric from the Weeknd",
help="Says a random lyric from the Weeknd from any of his albums")
# async def lyric(ctx, optional_alb=None):
async def weeknd(ctx):
  # await ctx.guild.me.edit(nick="El Fin de Semana")
  # if optional_alb == None:
  #   lyric = get_lyric("w", "")
  # else:
  #   lyric = get_lyric("w", optional_alb)
  async with ctx.message.channel.typing():
    lyric = get_lyric("w")
    embed = discord.Embed(title=lyric["song_name"], url = lyric["song_url"], description=lyric["lyric"], color=(lyric["album_color"]) )
    embed.set_thumbnail(url=lyric["album_art"])
    embed.add_field(name="\u200B", value="[{0}]({1})".format(lyric["album_name"], lyric['album_url']), inline=False)
    embed.add_field(name="\u200B", value=":musical_note: [Spotify]({})".format(get_spotify_url(f"the weeknd {lyric['song_name']}")), inline=False)
    # await asyncio.sleep(5)
    # await ctx.guild.me.edit(nick="Kanye Weast")
    await ctx.send(embed=embed)

@bot.command(aliases=["drizzy","papi"],
brief="Says a Drake lyric",
help="Says a random Drake lyric from any of his albums")
async def drake(ctx):
  async with ctx.message.channel.typing():
    lyric = get_lyric("d")
    embed = discord.Embed(title=lyric["song_name"], url = lyric["song_url"], description=lyric["lyric"], color=(lyric["album_color"]) )
    embed.set_thumbnail(url=lyric["album_art"])
    embed.add_field(name="\u200B", value="[{0}]({1})".format(lyric["album_name"], lyric['album_url']), inline=False)
    embed.add_field(name="\u200B", value=":musical_note: [Spotify]({})".format(get_spotify_url(lyric["song_name"])), inline=False)
    await ctx.send(embed=embed)

@bot.command(aliases=["lyric","lyrics"], 
brief="Grabs the lyrics for a given song",
help="Displays lyrics for the song name given")
async def getlyrics(ctx):
  async with ctx.message.channel.typing():
    i = ctx.message.content.find(' ')
    to_search = ctx.message.content[i+1:]
    song_info = get_song_info(to_search)

    over_limit = False
    if len(song_info["lyrics"]) <= 4092:
      desc = song_info["lyrics"]
    else:
      desc = song_info["lyrics"][:4093] + '...'
      over_limit = True

    embed = discord.Embed(
    title=song_info["name"], 
    url=song_info["url"], 
    description=desc,
    color=song_info["color"])
    embed.set_thumbnail(url=song_info["thumbnail"])
    
    if over_limit:
      embed.add_field(name='\u200B', value="For the full lyrics, [click here]({0}).".format(song_info["url"]))

    await ctx.send(embed=embed)

@bot.command(name="add")
async def add(ctx, num):
  url = "test/{}-xxx".format(num)
  pokemon_info = get_national_dex(url)
  number = "{}".format(num).rjust(3, "0")
  found = False
  user = True
  if str(ctx.author.id) == keys['MY_ID']:
    caught_list = "caught_pokemon.txt"
  elif str(ctx.author.id) == keys['ID_VIVIAN']:
    caught_list = "caught_pokemon_vivian.txt"
  else:
    user = False
    await ctx.send("Add command will not work for you pleb")
  with open("{}".format(caught_list), "r") as f:
    if "{}\n".format(number) in f.read():
      found = True
      await ctx.send("#{0} - {1} already in caught pokemon".format(number, pokemon_info['name']))
  if (found == False) and (user == True):
    caught = open("{}".format(caught_list), "a+")
    caught.write("{}\n".format(number))
    caught.close()
    await ctx.send("Added #{0} - {1} to caught pokemon".format(number, pokemon_info['name']))

@bot.command(name="morning",
brief="Kanye says good morning",
help="Are you dumb what is there to understand")
async def morning(ctx):
  embed = discord.Embed()
  embed.set_image(url="https://c.tenor.com/p-Eu-N2OuXkAAAAd/kanye-kanye-west.gif")
  # embed.description='Good morning'
  await ctx.send(embed=embed)

@bot.command(name="pingchef",
brief="Pings all masterchefs",
help="Pings all masterchefs added to the chefs list via &add")
async def ping(ctx):
  chefs = loadlist("chefs.pkl")
  for chef in chefs:
    if re.match('\d{18}', chef) is not None:
      user = await bot.fetch_user(chef)
      await ctx.send(f"Call {user.mention} Gordon Ramsay :cook:")
    else:
      await ctx.send(f"Call {chef.strip()} Gordon Ramsay :cook:")

# @bot.command(name="ask")
# async def ask(ctx):
#     """Asks the user a question to confirm something."""
#     # We create the view and assign it to a variable so we can wait for it later.
#     view = Confirm()
#     await ctx.send('Do you want to continue?', view=view)
#     # Wait for the View to stop listening for input...
#     await view.wait()
#     if view.value is None:
#         print('Timed out...')
#     elif view.value:
#         print('Confirmed...')
#     else:
#         print('Cancelled...')

@bot.command(name="annoy", 
brief="Annoys mentioned user", 
help="Pings mentioned user the number of times specified")
async def annoy(ctx, user = None, num_str = None, opt_str = None):
  invalid_num = False
  in_range = True
  invalid_user = not user[0] == "<"
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

  annoy_string = " get annoyed <:Pepepunch:794437891648520224>" if (opt_str == None) else " " + opt_str
  if num == 1:
    await ctx.send(user + annoy_string)
  else:
    for i in range(num):
      sleepnum = randint(0, 1000)
      print(f"{sleepnum}, {pinged.display_name}, {num - i}") if flag else print(f"{sleepnum}, {user}, {num - i}")
      await asyncio.sleep(sleepnum)
      if invalid_user or invalid_num or not in_range:
        await ctx.send(user.mention + annoy_string + " " + str(num-i), delete_after=10)
      else:
        await ctx.send(user + annoy_string + " " + str(num-i), delete_after=10)

  await ctx.send("Have a nice day :kissing_heart:")
  

# time = datetime.datetime.now
# @tasks.loop(seconds=1)
# async def timer():
#   print("here")
#   channel = bot.get_channel(865346448980049920)
#   msg_sent = False
#   estH = time().hour - 4
#   while True:
#     if estH == 17:
#       if not msg_sent:
#         await channel.send('its ' + str(estH) + ":" + str(time().minute))
#         msg_sent = True
#     else:
#         msg_sent = False


# @bot.event
# async def on_message_join(member):
#     channel = bot.get_channel(890998814197047316)
#     embed=discord.Embed(title=f"Welcome {member.name}", description=f"Welcome to UTSC COM SCI {member.guild.name}! PoST is Hell, but we're all <:pepeOK:756640035750674483>") # F-Strings!
#     embed.set_thumbnail(url=member.avatar_url) # Set the embed's thumbnail to the member's avatar image!

#     await channel.send(embed=embed)

@bot.command(name = "addchef", brief = "Adds a user to ping command", help = "Adds a user to ping command, only works for Kanye's developers")
async def addchef(ctx, user):
  if str(ctx.author.id) == keys['MY_ID'] or str(ctx.author.id) == keys['ID_STARBOY']:
    chefs = loadlist("chefs.pkl")
    if user in chefs:
      await ctx.send("User already in chefs' list")
    else:
      chefs.insert(0,user)
      dumplist(chefs, "chefs.pkl")
      await ctx.send("User added to chefs' list")
  else:
    await ctx.send("This command will not work for you pleb. Pathetic.")


@bot.command(name = "removechef", brief = "Removes a user from ping command", help = "Removes a user from ping command, only works for Kanye's developers")
async def removechef(ctx, user):
  if str(ctx.author.id) == keys['MY_ID'] or str(ctx.author.id) == keys['ID_STARBOY']:
    chefs = loadlist("chefs.pkl")
    if user not in chefs:
      if (str(ctx.message.mentions[0].id) in chefs):
        chefs.remove(str(ctx.message.mentions[0].id))
        dumplist(chefs, "chefs.pkl")
        await ctx.send("User removed from chefs' list")
      else:
        print(user)
        print(chefs)
        await ctx.send("User not in chefs' list")
    else:
      chefs.remove(user)
      dumplist(chefs, "chefs.pkl")
      await ctx.send("User removed from chefs' list")
  else:
    await ctx.send("This command will not work for you pleb. Pathetic.")

@bot.command(name="remind", brief="Reminds about upcoming assessments for a course", help="Displays upcoming assessment for the course given the channel where the command is used. Displays a list of all asssessments or all upcoming assessments if opt=all or opt=upcoming")
async def remind(ctx, opt=""):
  sort_db()
  channel_name = ctx.message.channel.name
  key = ""
  for course in valid_courses:
    if course in channel_name:
      key = course
  if key != "":
    if key in db:
      data = db[key]
      assessments = list(data.keys())
      if opt == "all":
        msg = "**All assessments for " + key.upper() + ": **\n\n"
        for name in assessments:
          if data[name] != TBD_DATE:
            dt = parse_dt(data[name])
            msg += name + " on " + dt["month"] + " " + dt["day"] + ", " + dt["year"] + " at " + dt["hour"] + ":" + dt["min"] + " " + dt["ampm"] + "\n"
          else:
            msg += name + " on TBD" + " at TBD" +"\n"
        await ctx.send(msg)
      elif opt == "upcoming":
        now = est_now()
        msg = "**All upcoming assessments for " + key.upper() + ": **\n\n"
        for name in assessments:
          if data[name] >= now and data[name] != TBD_DATE:
            dt = parse_dt(data[name])
            msg += name + " on " + dt["month"] + " " + dt["day"] + ", " + dt["year"] + " at " + dt["hour"] + ":" + dt["min"] + " " + dt["ampm"] + "\n"
          elif data[name] == TBD_DATE:
            msg += name + " on TBD" + " at TBD" +"\n"
        if msg == "All upcoming assessments: \n":
           msg = "There are no upcoming assessments currently recorded for this course!"
        await ctx.send(msg)
      else:
        nearest_dt = find_nearest_upcoming(data.values())
        if nearest_dt != None and nearest_dt != TBD_DATE:
          name = list(data.keys())[list(data.values()).index(nearest_dt)]
          dt = parse_dt(nearest_dt)
          await ctx.send("**Upcoming assessment for " + key.upper() + ": **\n\n" + name + " on " + dt["month"] + " " + dt["day"] + ", " + dt["year"] + " at " + dt["hour"] + ":" + dt["min"] + " " + dt["ampm"])
        else:
          await ctx.send("There are no upcoming assessments currently recorded for this course!")
    else:
      await ctx.send("There are no assessments currently recorded for this course!")
  else:
    await ctx.send("This command only works in course channels pleb.")

@bot.command(name="play",
brief="Play donda chants",
help="Plays donda chants in the voice channel user is currently in.")
async def play(ctx):
    voice = ctx.author.voice
    if voice:
      voice_channel = voice.channel
      vc = await voice_channel.connect()
      vc.play(discord.FFmpegPCMAudio("Kanye West - Donda Chant.mp3"))
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
async def roast(ctx, user=None):
  with open("roasts.txt", "r") as f:
    lines = f.readlines()
    i = randint(0,len(lines))
    if user == None:
      await ctx.send(ctx.author.mention + ". " + lines[i])
    else:
      await ctx.send(user + ". " + lines[i])

@bot.command(name="homie",
brief="Sends homie pics",
help="Send random homie pic. Use &homie [homie name]. Use &listhomies for a list of names. Picks random homie if no arguement provided.")
async def homies(ctx, homie=""):
  homies = os.listdir('pics')
  homies.remove('amogus')
  homies.remove('hbk')
  if homie == "":
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

@bot.command(name="listhomies",
brief="Lists homies",
help="Prints list of homies currently in our directory for &homie.")
async def list(ctx, homie=""):
  homies = os.listdir('pics')
  homies.remove('amogus')
  homies.remove('hbk')
  msg = "```\n"
  for homie in homies:
    msg += homie + "\n"
  msg += "```"
  await ctx.send(msg)
  
@bot.command(name="addpic",
brief="Adds a new image to specified folder(s).",
help="Add a new image by adding the image as an attatchment and specifying a folder location(s) (homie name) or amogus for sus quotes. &addpic {foldername} {foldername} ... {foldername}")
async def addpic(ctx, *folders):
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

@bot.command(name="addfolder",
brief="Adds new folder to pics.",
help="Adds a new folder to be used for &homies.")
async def addfolder(ctx, folder=""):
  if folder == "":
    await ctx.send("please specify a folder.")
    return
  if folder in os.listdir('pics'):
    await ctx.send("folder already exists.")
    return
  os.mkdir(os.path.join('pics', folder))
  await ctx.send(f"folder {folder} added. use &addpic {folder} to add images.")

@bot.command(name="rmfolder",
brief="Removes a folder from pics.",
help="Removes a folder from pics. (dev only)")
async def rmfolder(ctx, folder=""):
  if not (str(ctx.author.id) == keys['MY_ID'] or str(ctx.author.id) == keys['ID_STARBOY']):
    await ctx.send("this command is dev only pleb.")
    return
  if folder == "":
    await ctx.send("please specify a folder.")
    return
  if folder not in os.listdir('pics'):
    await ctx.send("folder does not exist.")
    return
  shutil.rmtree(os.path.join('pics', folder))
  await ctx.send(f"folder {folder} removed.")

@bot.command(name="amogus",
brief="Sends sus message from server.",
help="Sends random sus message from server.")
async def sus(ctx):
  images = os.listdir('pics/amogus')
  i = random.randint(0,len(images)-1)
  await ctx.send(file=discord.File(os.path.join('pics/amogus',images[i])))

@bot.command(aliases=["sad"],
brief="Sends heartbroken quote/image.",
help="Sends heartbroken quote/image.")
async def hbk(ctx):
  images = os.listdir('pics/hbk')
  i = random.randint(0,len(images)-1)
  file = discord.File(os.path.join('pics/hbk',images[i]))
  text = images[i][:-3]
  if len(text) >= 40:
    await ctx.send(text, file=file)
  else:
    await ctx.send(file=file)

@bot.command(aliases=["penis", "dick", "dagger", "glizzy", "ydd", "cock", "schlong"],
brief="Shows your pp.",
help="Shows your pp.")
async def pp(ctx, user=""):
  if user == "":
    user = ctx.message.author.name
    if ctx.message.author.id == int(keys['ID_STARBOY']) or ctx.message.author.id == int(keys['MY_ID']):
      length = 30
    else:
      length = randint(0, 30)
  else:
    user = user.replace("<", "")
    user = user.replace(">", "")
    id = user.replace("@", "")
    mem = await bot.fetch_user(id)
    if mem.id == keys['ID_STARBOY'] or mem.id == keys['MY_ID']:
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

snipe_message_author = {}
snipe_message_content = {}

@bot.event
async def on_message_delete(message):
    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = [message.content]
    if message.attachments:
      snipe_message_content[message.channel.id].append(message.attachments[0])

@bot.command(name="snipe",
brief="Snipes last deleted message in channel.",
help="Reytrives and sends the most recently deleted message in the current channel.")
async def snipe(ctx):
    channel = ctx.channel
    try:
      pfp_url = snipe_message_author[channel.id].avatar.url
      em = discord.Embed(description=snipe_message_content[channel.id][0],
                        color=get_color(pfp_url))
      em.set_author(name=snipe_message_author[channel.id].name, icon_url=str(pfp_url))
      if len(snipe_message_content[channel.id]) == 2:
        em.set_image(url=snipe_message_content[channel.id][1])
      em.set_footer(text=f"Last deleted message in #{channel.name}")
      await ctx.send(embed=em)
    except KeyError:
      await ctx.send(f"There are no recently deleted messages in #{channel.name}")

bot.run(keys['TOKEN'])