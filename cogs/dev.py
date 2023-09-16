import json
import os
import pickle
import subprocess

import discord
from discord.ext import commands

class DevelopersOnly(commands.Cog):
    """This category is only for dev use. If you're not a dev and try to use you could be banned."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.banned_set = self.load_banned_set()
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

    @commands.command(
        name="test1",
        brief="Test command.",
        help="Test command.",
        aliases=["t1"],
    )
    async def test1(self, ctx: commands.Context, *, content: str):
        await ctx.send(content)
        
    # NOTE: This is depreciated after the Docker move, but I'm keeping it here for reference.
    # @commands.command(
    #     name="restart",
    #     brief="Restarts bot, ***Dev use only***",
    #     help="Restarts bot, don't use if you're not a dev, will not work.",
    # )
    # async def restart(self, ctx: commands.Context):
    #     await ctx.send("Restarting...")
    #     subprocess.call(self.keys["RUN_BOT"])

    @commands.command(
        name="getgit",
        brief="Gets git info from latest commit.",
        help="Prints commit message and hash of current commit.",
        aliases=["gitget"],
    )
    async def getgit(self, ctx: commands.Context):
        if os.environ.get("RUNNING_IN_DOCKER"):
            with open("commit_message.txt") as f:
                git_msg = f.read()
        else:
            git_msg = subprocess.check_output(
                ["git", "log", "-1", "--format='%s'"]
            ).decode("ascii").strip()
        await ctx.send(git_msg)

    @commands.command(
        name="delete",
        brief="Delete bot's latest message.",
        help="Deletes latest message that bot sent by default. Deletes up to the number provided. Only searches 20 messages up.",
    )
    async def delete(self, ctx: commands.Context, num: commands.Range[int, 0, 20] = 1, user: discord.User | discord.Member = None):
        if user and user.id == ctx.author.id:
            await ctx.send("You can't delete your own messages with the bot! Just delete them yourself")
            return

        msgs = [
            msg
            async for msg in ctx.channel.history(limit=20)
            if msg.author.id == self.bot.user.id or (user and msg.author.id == user.id)
        ]

        await ctx.message.delete()

        def ordinal(x: int) -> str:
            match x:
                case 0:
                    return "1st"
                case 1:
                    return "2nd"
                case 2:
                    return "3rd"
                case y if y > 2 or y <= 19:
                    return f"{y}th"
                case _:
                    return "nth"

        for i in range(num):
            try:
                latest_message = msgs.pop(0)
            except IndexError:
                latest_message = None

            if latest_message:
                await ctx.send(f"Deleting {ordinal(i)} latest message.", delete_after=2)
                await latest_message.delete()
            else:
                await ctx.send(f"{'Bot' if user is None else user.mention} hasn't sent a message recently.", delete_after=2)
                return

    @commands.command(
            name="ban",
            brief="Bans mentioned user(s)",
            help="Bans mentioned user(s) from using commands from the Miscellaneous cog"
    )
    async def ban(self, ctx: commands.Context):
       if ctx.message.mentions:
           for user in ctx.message.mentions:
               await self.ban_user(ctx, user)

    @commands.command(
            name="unban",
            brief="Unbans mentioned user(s)",
            help="Unbans mentioned user(s) from using commands from the Miscellaneous cog"
    )
    async def unban(self, ctx: commands.Context):
       if ctx.message.mentions:
           for user in ctx.message.mentions:
               await self.unban_user(ctx, user)

    async def ban_user(self, ctx: commands.Context, user: discord.User | discord.Member):
        self.banned_set.add(user.id)
        with open("banned_users.pkl", "wb") as f:
            pickle.dump(self.banned_set, f)
        await ctx.send(f"{user.mention} banned")

    async def unban_user(self, ctx: commands.Context, user: discord.User | discord.Member):
        try:
            self.banned_set.remove(user.id)
            with open("banned_users.pkl", "wb") as f:
                pickle.dump(self.banned_set, f)
        except KeyError:
            await ctx.send(f"{user.mention} not in banned set.")
            return
        await ctx.send(f"{user.mention} unbanned")

    def load_banned_set(self) -> set[int]:
        if not os.path.isfile("banned_users.pkl"):
            with open("banned_users.pkl", "wb") as f:
                pickle.dump(set(), f)
        with open("banned_users.pkl", "rb") as f:
            try:
                banned_set = pickle.load(f)
                return banned_set
            except EOFError:
                return set()

    @commands.command(
        name="showban",
        brief="Show banned users",
        help="Show banned users",
    )
    async def showban(self, ctx: commands.Context):
        if ctx.guild:
            name_function = lambda id: ctx.guild.get_member(id).display_name
        else:
            name_function = lambda id: self.bot.get_user(id).name
        banned_list = "```\n"
        banned_list += "\n".join(map(name_function, self.banned_set)) if self.banned_set else "No banned users yet."
        banned_list += "\n```"
        await ctx.send(banned_list)
        
    @commands.command(
        name="toggle",
        brief="toggles specified command",
        help="toggles specified command",
    )
    async def toggle(self, ctx: commands.Context, command_str: str):
        command = self.bot.get_command(command_str)

        if command is None:
            embed = discord.Embed(title="ERROR", description="I can't find a command with that name!", color=0xff0000)
            await ctx.send(embed=embed)

        elif ctx.command == command:
            embed = discord.Embed(title="ERROR", description="You cannot disable this command.", color=0xff0000)
            await ctx.send(embed=embed)

        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            embed = discord.Embed(title="Toggle", description=f"I have {ternary} {command.qualified_name} for you!", color=0xff00c8)
            await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(DevelopersOnly(bot))
