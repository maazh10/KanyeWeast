import discord
from discord.ext import commands

from cogs.utils import get_color

import requests
import json

class Miscellaneous(commands.Cog):
    """Rando stuff."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def get_quote(self):
        response = requests.get("https://api.kanye.rest")
        json_data = json.loads(response.text)
        return json_data["quote"]

    @commands.command(
    name="hello",
    brief="Says hello",
    help="Says hello to whoever used the `hello` command"
    )
    async def hello(self, ctx: commands.Context):
        if await self.bot.is_owner(ctx.author):
            if ctx.message.content.endswith('son'):
                await ctx.send('Hello master!')
            else:
                await ctx.send('Hello ' + ctx.author.display_name + '!')
        else:
            if ctx.message.content.endswith('dad'):
                await ctx.send('Hello son!')
            else:
                await ctx.send('Hello '+ ctx.author.display_name + '!')

    @commands.command(
    aliases=["donda?", "donda"],
    brief="Says whether Donda is out or not",
    help="Says whether Donda is out or not (long version)"
    )
    async def rembr(self, ctx: commands.Context):
        await ctx.send('i rember <:3736_GalaxyBrainPepe:769650997681061950>')
        embed = discord.Embed()
        embed.description = '[Out 2021](https://music.apple.com/us/album/donda/1583449420)'
        await ctx.send(embed=embed)

    @commands.command(name="quote",
    brief="Says a Kanye quote",
    help="Says a Kanye quote using a Kanye quote API"
    )
    async def quote(self, ctx: commands.Context):
        embed = discord.Embed()
        pfp_url = self.bot.user.avatar.url
        embed.color = await get_color(pfp_url)
        embed.set_author(name="Kanye West", icon_url=pfp_url)
        embed.description='[{}](https://www.youtube.com/watch?v=dQw4w9WgXcQ)'.format(self.get_quote())
        await ctx.send(embed=embed)

    @commands.command(name="rick",
    brief="Get Rick'd",
    help="Are you dumb what is there to understand")
    async def rick(self, ctx: commands.Context):
        embed = discord.Embed()
        embed.set_image(url="https://media1.tenor.com/images/3e30fa16b8a79b44185060d0df450009/tenor.gif?itemid=19920902")
        embed.description='Never gonna give you up'
        await ctx.send(embed=embed, delete_after=8)

    @commands.command(name="morning",
    brief="Kanye says good morning",
    help="Are you dumb what is there to understand")
    async def morning(self, ctx: commands.Context):
        embed = discord.Embed()
        embed.set_image(url="https://tenor.com/view/alarm-wake-up-tired-so-gif-24728280.gif")
        await ctx.send(embed=embed)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Miscellaneous(bot))