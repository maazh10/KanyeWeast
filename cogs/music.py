import discord
from discord.ext import commands

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from random import randint
import lyricsgenius
import unicodedata
from asyncio import sleep
import sys
import traceback

from cogs.utils import get_color, UserBanned


class Music(commands.Cog):
    """This category has all music related commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("secrets.json") as f:
            self.keys = json.load(f)

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

    def get_spotify_url(self, artist: str, song_name: str, album: str):
        sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=self.keys["SPOTIFY_CLIENT_ID"],
                client_secret=self.keys["SPOTIFY_CLIENT_SECRET"],
            )
        )
        results = sp.search(
            q=unicodedata.normalize(
                "NFKD", f"{song_name}&album:{album}&artist:{artist}"
            ),
            limit=5,
        )
        return results["tracks"]["items"][0]["external_urls"]["spotify"]

    def get_lyric(self, k_or_w_or_d: str):
        if k_or_w_or_d == "k":
            all_albums = {
                0: [
                    "Lyrics_TheCollegeDropout_withList.json",
                    "The College Dropout",
                    4331796,
                ],
                1: [
                    "Lyrics_808sHeartbreak_withList.json",
                    "808s and Heartbreak",
                    12897227,
                ],
                2: ["Lyrics_Graduation_withList.json", "Graduation", 10112126],
                3: ["Lyrics_JESUSISKING_withList.json", "Jesus Is King", 402108],
                4: [
                    "Lyrics_KanyeWestPresentsGoodMusicCruelSummer_withList.json",
                    "Good Music, Cruel Summer",
                    14803425,
                ],
                5: ["Lyrics_KIDSSEEGHOSTS_withList.json", "KIDS SEE GHOSTS", 12890526],
                6: [
                    "Lyrics_LateRegistration_withList.json",
                    "Late Registration",
                    1511179,
                ],
                7: [
                    "Lyrics_MyBeautifulDarkTwistedFantasy_withList.json",
                    "My Beautiful Dark Twisted Fantasy",
                    15345470,
                ],
                8: [
                    "Lyrics_TheLifeofPablo_withList.json",
                    "The Life of Pablo",
                    16026708,
                ],
                9: [
                    "Lyrics_WatchtheThrone_withList.json",
                    "Watch the Throne",
                    15238995,
                ],
                10: ["Lyrics_ye_withList.json", "ye", 13092804],
                11: ["Lyrics_Yeezus_withList.json", "Yeezus", 6955557],
                12: ["Lyrics_Donda_withList.json", "Donda", 2463422],
            }
        elif k_or_w_or_d == "w":
            all_albums = {
                0: ["Lyrics_AfterHours_withList.json", "After Hours", 2104082],
                1: [
                    "Lyrics_BeautyBehindtheMadness_withList.json",
                    "Beauty Behind the Madness",
                    13026239,
                ],
                2: [
                    "Lyrics_EchoesofSilence_withList.json",
                    "Echoes of Silence",
                    2300954,
                ],
                3: [
                    "Lyrics_HouseofBalloons_withList.json",
                    "House of Balloons",
                    3289393,
                ],
                4: ["Lyrics_KissLand_withList.json", "Kiss Land", 792342],
                5: ["Lyrics_Starboy_withList.json", "Starboy", 13711403],
                6: ["Lyrics_Thursday_withList.json", "Thursday", 15197149],
                7: ["Lyrics_Trilogy_withList.json", "Trilogy", 460551],
                8: ["Lyrics_DawnFM_withList.json", "Dawn FM", 3569036],
            }
        # if (album == ""):
        elif k_or_w_or_d == "d":
            all_albums = {
                0: ["Lyrics_CarePackage_withList.json", "Care Package", 460552],
                1: [
                    "Lyrics_CertifiedLoverBoy_withList.json",
                    "Certified Lover Boy",
                    12344040,
                ],
                2: [
                    "Lyrics_HonestlyNevermind_withList.json",
                    "Honestly Nevermind",
                    921616,
                ],
                3: ["Lyrics_ComebackSeason_withList.json", "Comeback Season", 12287806],
                4: [
                    "Lyrics_DarkLaneDemoTapes_withList.json",
                    "Dark Lane Demo Tapes",
                    1382408,
                ],
                5: [
                    "Lyrics_IfYoureReadingThisItsTooLate_withList.json",
                    "If You're Reading This It's Too Late",
                    14408925,
                ],
                6: ["Lyrics_MoreLife_withList.json", "More Life", 12686196],
                7: [
                    "Lyrics_NothingWastheSame_withList.json",
                    "Nothing Was The Same",
                    3707854,
                ],
                8: [
                    "Lyrics_RoomforImprovement_withList.json",
                    "Room For Improvement",
                    1710877,
                ],
                9: ["Lyrics_ScaryHours_withList.json", "Scary Hours", 2631720],
                10: ["Lyrics_SoFarGone_withList.json", "So Far Gone", 263172],
                11: ["Lyrics_ThankMeLater_withList.json", "Thank Me Later", 525573],
                12: [
                    "Lyrics_TheBestintheWorldPack_withList.json",
                    "The Best In The World Pack",
                    394758,
                ],
                13: ["Lyrics_Views_withList.json", "Views", 6056047],
                14: [
                    "Lyrics_WhataTimeToBeAlive_withList.json",
                    "What a Time To Be Alive",
                    12895432,
                ],
                15: ["Lyrics_Scorpion_withList.json", "Scorpion", 3355443],
                16: ["Lyrics_TakeCare_withList.json", "Take Care", 11769461],
            }
        else:
            return

        albumnumber = randint(0, len(all_albums) - 1)
        file = open("lyrics/{0}/{1}".format(k_or_w_or_d, all_albums[albumnumber][0]))
        data = json.load(file)
        songnumber = randint(0, len(data["tracks"]) - 1)
        lyricnumber = randint(0, len(data["tracks"][songnumber]["song"]["lyrics"]) - 1)
        return_dict = {
            "lyric": data["tracks"][songnumber]["song"]["lyrics"][lyricnumber],
            "album_art": data["cover_art_url"],
            "album_name": data["name"],
            "song_name": data["tracks"][songnumber]["song"]["title_with_featured"],
            "album_url": data["url"],
            "song_url": data["tracks"][songnumber]["song"]["url"],
            "album_color": all_albums[albumnumber][-1],
        }
        file.close()
        return return_dict

    def clean_lyric_footer(self, lyric: str):
        i = lyric.find("Embed") - 1
        if i != -1:
            if lyric[i - 2 : i].isnumeric():
                lyric = lyric[: i - 2]
            elif lyric[i - 1 : i].isnumeric():
                lyric = lyric[: i - 1]
            elif lyric[i].isnumeric():
                lyric = lyric[:i]
        return lyric

    async def get_song_info(self, to_search: str):
        genius = lyricsgenius.Genius(self.keys["GENIUS_TOKEN"])
        song = genius.search_song(to_search)
        lyrics = self.clean_lyric_footer(song.lyrics)
        return {
            "name": song.full_title,
            "url": song.url,
            "lyrics": lyrics,
            "color": get_color(song.header_image_thumbnail_url),
            "thumbnail": song.header_image_thumbnail_url,
        }

    async def send_lyric(self, type: str, ctx: commands.Context):
        type_dict = {"k": "Kanye West", "w": "The Weeknd", "d": "Drake"}
        async with ctx.message.channel.typing():
            lyric = self.get_lyric(type)
            embed = discord.Embed(
                title=lyric["song_name"],
                url=lyric["song_url"],
                description=lyric["lyric"],
                color=(lyric["album_color"]),
            )
            embed.set_thumbnail(url=lyric["album_art"])
            embed.add_field(
                name="\u200B",
                value="[{0}]({1})".format(lyric["album_name"], lyric["album_url"]),
                inline=False,
            )
            embed.add_field(
                name="\u200B",
                value=":musical_note: [Spotify]({})".format(
                    self.get_spotify_url(
                        type_dict[type], lyric["song_name"], lyric["album_name"]
                    )
                ),
                inline=False,
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="bar",
        brief="Says a Kanye lyric",
        help="Says a random Kanye lyric from any of his albums",
    )
    async def bar(self, ctx: commands.Context):
        await self.send_lyric("k", ctx)

    @commands.command(
        name="weeknd",
        brief="Says a lyric from the Weeknd",
        help="Says a random lyric from the Weeknd from any of his albums",
    )
    async def weeknd(self, ctx: commands.Context):
        await self.send_lyric("w", ctx)

    @commands.command(
        aliases=["drizzy", "papi"],
        brief="Says a Drake lyric",
        help="Says a random Drake lyric from any of his albums",
    )
    async def drake(self, ctx: commands.Context):
        await self.send_lyric("d", ctx)

    @commands.command(
        aliases=["lyric", "lyrics"],
        brief="Grabs the lyrics for a given song",
        help="Displays lyrics for the song name given",
    )
    async def getlyrics(self, ctx: commands.Context):
        async with ctx.message.channel.typing():
            i = ctx.message.content.find(" ")
            to_search = ctx.message.content[i + 1 :]
            song_info = await self.get_song_info(to_search)

            over_limit = False
            if len(song_info["lyrics"]) <= 4092:
                desc = song_info["lyrics"]
            else:
                desc = song_info["lyrics"][:4093] + "..."
                over_limit = True

            embed = discord.Embed(
                title=song_info["name"],
                url=song_info["url"],
                description=desc,
                color=song_info["color"],
            )
            embed.set_thumbnail(url=song_info["thumbnail"])

        if over_limit:
            embed.add_field(
                name="\u200B",
                value="For the full lyrics, [click here]({0}).".format(
                    song_info["url"]
                ),
            )

        await ctx.send(embed=embed)

    @commands.command(
        name="play",
        brief="Play donda chants",
        help="Plays donda chants in the voice channel user is currently in.",
    )
    async def play(self, ctx: commands.Context):
        if ctx.author.voice:
            voice = ctx.author.voice
            voice_channel = voice.channel
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio("play.mp3"))
            song_info = self.get_song_info("Donda Chant")
            embed = discord.Embed(
                title=song_info["name"],
                url=song_info["url"],
                description=song_info["lyrics"],
                color=song_info["color"],
            )
            embed.set_thumbnail(url=song_info["thumbnail"])
            await ctx.send(embed=embed)
            while vc.is_playing():
                await sleep(0.1)
            await vc.disconnect()
        else:
            await ctx.send("You are not in a voice channel pleb.")

    @commands.command(
        name="",
        brief="Sends hbk song.",
        help="Sends hbk song from a special playlist :)",
    )
    async def hbk(self, ctx: commands.Context):
        sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=self.keys["SPOTIFY_CLIENT_ID"],
                client_secret=self.keys["SPOTIFY_CLIENT_SECRET"],
            )
        )

        playlist_id = "7xMtk8dsPZCpQhASkO9Uvi?si=5ad1144294014dec"
        results = sp.playlist(playlist_id)
        items = results["tracks"]["items"]
        rnd = randint(0, len(items))
        song_url = items[rnd]["track"]["external_urls"]["spotify"]
        await ctx.send(song_url)


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
