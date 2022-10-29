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
            subprocess.check_output("git log -1 --format=%h %s").decode("ascii").strip()
        )

    @commands.command(
        name="delete",
        brief="Delete bot's latest message.",
        help="Deletes latest message that bot sent. Only searches 20 messages up.",
    )
    async def delete(self, ctx: commands.Context):
        bot_msgs = [
            msg
            async for msg in ctx.channel.history(limit=20)
            if msg.author.id == self.bot.user.id
        ]
        latest_message = bot_msgs[0] if len(bot_msgs) > 0 else None
        await ctx.message.delete()
        if latest_message:
            await ctx.send("Deleting latest message", delete_after=5)
            await latest_message.delete()
        else:
            await ctx.send("Bot hasn't sent a message recently.")
            return


async def setup(bot: commands.Bot):
    await bot.add_cog(DevelopersOnly(bot))
