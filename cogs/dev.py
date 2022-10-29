import discord
from discord.ext import commands
import subprocess
import json


class DevelopersOnly(commands.Cog):
    """This category is only for dev use. If you're not a dev and try to use you could be banned."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        with open("secrets.json") as f:
            self.keys = json.load(f)

    async def cog_check(self, ctx: commands.Context):
        return await self.bot.is_owner(ctx.author)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"We have logged in as {self.bot.user}")

    @commands.command()
    async def shutdown(self, ctx: commands.Context):
        await ctx.send("Shutting down...")
        exit()

    @commands.command()
    async def test(self, ctx: commands.Context):
        await ctx.send("Hello dev")

    @commands.command(
        name="restart",
        brief="Restarts bot, ***Dev use only***",
        help="Restarts bot, don't use if you're not a dev, will not work.",
    )
    async def restart(self, ctx: commands.Context):
        await ctx.send("Restarting...")
        subprocess.call(self.keys["RUN_BOT"])

    @commands.command(
        name="getgit",
        brief="Gets git info from latest commit.",
        help="Prints commit message and hash of current commit.",
    )
    async def getgit(self, ctx: commands.Context):
        await ctx.send(
            subprocess.check_output(["git", "log", "-1", "--format='%h %s'"])
            .decode("ascii")
            .strip()
        )

    @commands.command(
        name="delete",
        brief="Delete bot's latest message.",
        help="Deletes latest message that bot sent by default. Deletes up to the number provided. Only searches 20 messages up.",
    )
    async def delete(self, ctx: commands.Context, num=1):
        bot_msgs = [
            msg
            async for msg in ctx.channel.history(limit=20)
            if msg.author.id == self.bot.user.id
        ]
        await ctx.message.delete()
        for i in range(num):
            try:
                latest_message = bot_msgs.pop(0)
            except IndexError:
                latest_message = None

            if latest_message:
                ordinal = lambda x: [
                    "1st",
                    "2nd",
                    "3rd",
                    "4th",
                    "5th",
                    "6th",
                    "7th",
                    "8th",
                    "9th",
                    "10th",
                    "11th",
                    "12th",
                    "13th",
                    "14th",
                    "15th",
                    "16th",
                    "17th",
                    "18th",
                    "19th",
                    "20th",
                ][x]
                await ctx.send(f"Deleting {ordinal(i)} latest message.", delete_after=2)
                await latest_message.delete()
            else:
                await ctx.send("Bot hasn't sent a message recently.")
                return


async def setup(bot: commands.Bot):
    await bot.add_cog(DevelopersOnly(bot))
