import discord
from discord.ext import commands

from cogs.utils import get_color, category_map

import requests
import json
import random
import html
import time
import sqlite3

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
        help="Says hello to whoever used the `hello` command",
    )
    async def hello(self, ctx: commands.Context):
        if await self.bot.is_owner(ctx.author):
            if ctx.message.content.endswith("son"):
                await ctx.send("Hello master!")
            else:
                await ctx.send(f"Hello {ctx.author.display_name}!")
        else:
            if ctx.message.content.endswith("dad"):
                await ctx.send("Hello son!")
            else:
                await ctx.send(f"Hello {ctx.author.display_name}!")

    @commands.command(
        aliases=["donda?", "donda"],
        brief="Says whether Donda is out or not",
        help="Says whether Donda is out or not (long version)",
    )
    async def rembr(self, ctx: commands.Context):
        await ctx.send("i rember <:3736_GalaxyBrainPepe:769650997681061950>")
        embed = discord.Embed()
        embed.description = (
            "[Out 2021](https://music.apple.com/us/album/donda/1583449420)"
        )
        await ctx.send(embed=embed)

    @commands.command(
        name="quote",
        brief="Says a Kanye quote",
        help="Says a Kanye quote using a Kanye quote API",
    )
    async def quote(self, ctx: commands.Context):
        embed = discord.Embed()
        assert self.bot.user is not None
        assert self.bot.user.avatar
        pfp_url = self.bot.user.avatar.url
        embed.color = await get_color(pfp_url)
        embed.set_author(name="Kanye West", icon_url=pfp_url)
        embed.description = "[{}](https://www.youtube.com/watch?v=dQw4w9WgXcQ)".format(
            self.get_quote()
        )
        await ctx.send(embed=embed)

    @commands.command(
        name="rick", brief="Get Rick'd", help="Are you dumb what is there to understand"
    )
    async def rick(self, ctx: commands.Context):
        embed = discord.Embed()
        embed.set_image(
            url="https://media1.tenor.com/images/3e30fa16b8a79b44185060d0df450009/tenor.gif?itemid=19920902"
        )
        embed.description = "Never gonna give you up"
        await ctx.send(embed=embed, delete_after=8)

    @commands.command(
        name="morning",
        brief="Kanye says good morning",
        help="Are you dumb what is there to understand",
    )
    async def morning(self, ctx: commands.Context):
        embed = discord.Embed()
        embed.set_image(
            url="https://tenor.com/view/alarm-wake-up-tired-so-gif-24728280.gif"
        )
        await ctx.send(embed=embed)

    @commands.command(
        aliases=["triv"],
        brief="Play a round of trivia",
        help="Play a round of trivia. Choose a category with &trivia {category}. To view a list of categories use &trivia categories. If no category is specified, a random category will be chosen.",
    )
    async def trivia(self, ctx: commands.Context, category: str = ""):
        if category == "leaderbord" or category == "lb":
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            sql = '''
                SELECT user_id, easy + medium + hard AS score 
                FROM TriviaLB 
                WHERE guild_id = ? 
                ORDER BY score DESC
            '''
            c.execute(sql, [ctx.guild.id])
            embed = discord.Embed(title=f'Leaderboard - {ctx.guild}', color = discord.Colour.random())
            embed.set_thumbnail(url=ctx.guild.icon.url)
            rank = 1
            board = "```"
            for row in c.fetchall():
                user = await ctx.guild.fetch_member(row[0])
                score = row[1]
                board += f'{score}\t{user.display_name:<30}\n'
                rank += 1
            board += "```"
            embed.description = board
            await ctx.send(embed=embed)
            conn.close()
            return
        if category == "categories":
            embed = discord.Embed(title='Categories', description=f'General\nBooks\nFilm\nMusic\nTheatre\nTelevision\nVideo Games\nBoard Games\nNature\nComputers\nMath\nMythology\nSports\nGeography\nHistory\nPolitics\nArt\nCelebrities\nAnimals\nVehicles\nComics\nGadgets\nAnime\nCartoon', color = discord.Colour.random())
            await ctx.send(embed=embed)
            return
        start = time.time()
        response = requests.get(f'https://opentdb.com/api.php?amount=1') 
        if category:
            if category_map(category):
                cat_id = category_map(category)
                response = requests.get(f'https://opentdb.com/api.php?amount=1&category={cat_id}') 
            else:
                await ctx.send("Invalid category. Please enter a valid category.")
                return
        if response.status_code == 200:
            data = response.json()["results"][0]
            answers = data["incorrect_answers"]
            answers.append(data["correct_answer"])
            random.shuffle(answers)
            choices = ""
            for i in range(97, 97+len(answers)):
                choices += f"\n({chr(i)}) {html.unescape(answers[i - 97])}\n"
            embed = discord.Embed(title='Question', description=f'{html.unescape(data["question"])}', color = discord.Colour.random())
            embed.add_field(name='Difficulty', value=f'{data["difficulty"].capitalize()}', inline=True)
            embed.add_field(name='Category', value=f'{data["category"]}', inline=True)
            embed.add_field(name='Choices', value=f'{choices}', inline=False)
            await ctx.send(embed=embed)
            response = await self.bot.wait_for('message')
            message_predicate = response.author.id == ctx.message.author.id and response.channel.id == ctx.message.channel.id
            while not message_predicate:
                response = await self.bot.wait_for('message')
                message_predicate = response.author.id == ctx.message.author.id and response.channel.id == ctx.message.channel.id
            response_list = ["a", "b", "c", "d"] if len(answers) == 4 else ["a", "b"]
            if response.content.lower() not in response_list:
                await response.reply(f"Invalid response bozo, correct answer was **{html.unescape(data['correct_answer'])}**")
                return
            if time.time() - start > 20:
                await response.reply(f"You took too long to answer bozo, correct answer was **{html.unescape(data['correct_answer'])}**")
                return
            if answers[ord(response.content.lower()) - 97] == data["correct_answer"]:
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                sql = "SELECT * FROM TriviaLB WHERE user_id = ? AND guild_id = ?"
                cursor.execute(sql, (ctx.author.id, ctx.guild.id))
                if cursor.fetchone():
                    sql = f"UPDATE TriviaLB SET {data['difficulty']} = {data['difficulty']} + 1 WHERE user_id = ? AND guild_id = ?"
                    cursor.execute(sql, (ctx.author.id, ctx.guild.id))
                    conn.commit()
                else: 
                    sql = f"INSERT INTO TriviaLB (user_id, guild_id, {data['difficulty']}) VALUES (?, ?, ?)"
                    cursor.execute(sql, (ctx.author.id, ctx.guild.id, 1))
                    conn.commit()
                conn.close()
                await response.reply("Correct!")
            else:
                await response.reply(f"Wrong bozo, it was **{html.unescape(data['correct_answer'])}**")
        else:
            await ctx.send(f'Request failed with status code {response.status_code}')
    

async def setup(bot: commands.Bot):
    await bot.add_cog(Miscellaneous(bot))
