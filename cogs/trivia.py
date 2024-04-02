import asyncio
import html
import json
import random
import sqlite3
import time

import boto3
import discord
import requests
from discord.ext import commands

from cogs.dev import DevelopersOnly
from cogs.utils import UserBanned, category_map


class TriviaCog(commands.Cog):
    """All trivia related commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.users = {}
        with open("secrets.json", "r") as f:
            self.secrets = json.load(f)

    ##############################
    ####### COG BAN CHECK ########
    ##############################

    async def cog_check(self, ctx: commands.Context) -> bool:
        dev = self.bot.get_cog("DevelopersOnly")
        assert isinstance(dev, DevelopersOnly)
        if ctx.author.id in dev.banned_set:
            raise UserBanned(ctx.message.author)
        return True

    ##############################
    ##############################
    ##############################

    def update_db_file(self):
        s3 = boto3.client("s3")
        bucket = "kanyeweastcredentials"
        s3.upload_file("database.db", bucket, "database.db")

    async def get_user_name(self, ctx: commands.Context, row: tuple) -> str:
        user_id = row[0]
        score = row[1]
        user_name = ""
        user = None
        if self.users.get(user_id, ""):
            user_name = self.users[user_id]
        else:
            try:
                try:
                    user = await ctx.guild.fetch_member(user_id)
                    user_name = user.display_name
                except discord.NotFound:
                    user = self.bot.get_user(user_id)
                    await ctx.send(f"User {user.name} not in server")
                    user_name = user.name
                self.users[user_id] = user_name
            except AttributeError:
                return ""
        return f"{score: <3}\t{user_name: <30}\n"

    async def get_leaderboard(self, ctx: commands.Context):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        sql = """
            SELECT user_id, easy + medium + hard AS score 
            FROM TriviaLB 
            WHERE guild_id = ? 
            ORDER BY score DESC
        """
        c.execute(sql, [ctx.guild.id])
        embed = discord.Embed(
            title=f"Leaderboard - {ctx.guild}", color=discord.Colour.random()
        )
        embed.set_thumbnail(url=ctx.guild.icon.url)
        board = "```"
        display_names = map(lambda row: self.get_user_name(ctx, row), c.fetchall())
        display_names = await asyncio.gather(*display_names)
        board += "".join(display_names)
        board += "```"
        embed.description = board
        await ctx.send(embed=embed)
        conn.close()
        self.update_db()
        return

    def update_db(
        self, ctx: commands.Context, user_id: int, difficulty: str, correct: bool
    ):
        """Connects to the database and updates the leaderboard.

        Args:
            ctx: command context
            user_id: user id to update
            difficulty: difficulty level
            correct: if the user got the question correct
        """
        assert ctx.guild is not None
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        sql = "SELECT * FROM TriviaLB WHERE user_id = ? AND guild_id = ?"
        cursor.execute(sql, (ctx.author.id, ctx.guild.id))
        if cursor.fetchone():
            if correct:
                sql = f"UPDATE TriviaLB SET {difficulty} = {difficulty} + 1 WHERE user_id = ? AND guild_id = ?"
                cursor.execute(sql, (ctx.author.id, ctx.guild.id))
            else:
                sql = f"INSERT INTO TriviaLB (user_id, guild_id, {difficulty}) VALUES (?, ?, ?)"
                cursor.execute(sql, (ctx.author.id, ctx.guild.id, 1))
        else:
            sql = f"UPDATE TriviaLB SET {difficulty} = {difficulty} - 1 WHERE user_id = ? AND guild_id = ? AND {difficulty} > 0"
            cursor.execute(sql, (ctx.author.id, ctx.guild.id))
        conn.commit()
        conn.close()

    @commands.command(
        aliases=["triv"],
        brief="Play a round of trivia",
        help="Play a round of trivia. Choose a category with &trivia {category}. To view a list of categories use &trivia categories. If no category is specified, a random category will be chosen.",
    )
    async def trivia(self, ctx: commands.Context, category: str = ""):
        if category == "leaderboard" or category == "lb":
            await self.get_leaderboard(ctx)
            return
        if category == "categories":
            embed = discord.Embed(
                title="Categories",
                description="General\nBooks\nFilm\nMusic\nTheatre\nTelevision\nVideo Games\nBoard Games\nNature\nComputers\nMath\nMythology\nSports\nGeography\nHistory\nPolitics\nArt\nCelebrities\nAnimals\nVehicles\nComics\nGadgets\nAnime\nCartoon",
                color=discord.Colour.random(),
            )
            await ctx.send(embed=embed)
            return
        start = time.time()
        if category:
            if category_map(category):
                cat_id = category_map(category)
                response = requests.get(
                    f"https://opentdb.com/api.php?amount=1&category={cat_id}"
                )
            else:
                await ctx.send("Invalid category. Please enter a valid category.")
                return
        else:
            response = requests.get("https://opentdb.com/api.php?amount=1")
        if response.status_code == 200:
            data = response.json()["results"][0]
            if data["type"] == "multiple":
                answers = data["incorrect_answers"]
                answers.append(data["correct_answer"])
                random.shuffle(answers)
            else:
                answers = ["True", "False"]
            choices = ""
            for i in range(97, 97 + len(answers)):
                choices += f"\n({chr(i)}) {html.unescape(answers[i - 97])}\n"
            embed = discord.Embed(
                title="Question",
                description=f'{html.unescape(data["question"])}',
                color=discord.Colour.random(),
            )
            embed.add_field(
                name="Difficulty",
                value=f'{data["difficulty"].capitalize()}',
                inline=True,
            )
            embed.add_field(name="Category", value=f'{data["category"]}', inline=True)
            embed.add_field(name="Choices", value=f"{choices}", inline=False)
            await ctx.send(embed=embed)
            response_list = ["a", "b", "c", "d"] if len(answers) == 4 else ["a", "b"]
            response = await self.bot.wait_for("message")
            message_predicate = (
                response.author.id == ctx.message.author.id
                and response.channel.id == ctx.message.channel.id
                and response.content.lower() in response_list
            )
            while not message_predicate:
                response = await self.bot.wait_for("message")
                message_predicate = (
                    response.author.id == ctx.message.author.id
                    and response.channel.id == ctx.message.channel.id
                    and response.content.lower() in response_list
                )
            if time.time() - start > 20:
                await response.reply(
                    f"You took too long to answer bozo, correct answer was **{html.unescape(data['correct_answer'])}**"
                )
                return
            if answers[ord(response.content.lower()) - 97] == data["correct_answer"]:
                await response.reply("Correct!")
                self.update_db(ctx, ctx.author.id, data["difficulty"], True)
            else:
                await response.reply(
                    f"Wrong bozo, it was **{html.unescape(data['correct_answer'])}**"
                )
                self.update_db(ctx, ctx.author.id, data["difficulty"], False)
        else:
            await ctx.send(f"Request failed with status code {response.status_code}")


async def setup(bot: commands.Bot):
    await bot.add_cog(TriviaCog(bot))
