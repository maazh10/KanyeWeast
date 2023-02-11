from discord.ext import commands
import discord
import subprocess
import json
import pickle
import os
import sys
import traceback

class DevelopersOnly(commands.Cog):
    """This category is only for dev use. If you're not a dev and try to use you could be banned."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.banned_set = self.load_banned_set()
        with open("secrets.json") as f:
            self.keys = json.load(f)

    async def cog_check(self, ctx: commands.Context):
        return await self.bot.is_owner(ctx.author)

    ##################################################################################################
    ####################################### COG ERROR HANDLER ########################################
    ##################################################################################################

    async def cog_command_error(self, ctx, error: commands.CommandError):
        if hasattr(ctx.command, "on_error"):
            return

        ignored = ()

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, "original", error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CheckFailure):
            await ctx.send("This command is dev-only pleb.")
            return

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print(
                "Ignoring exception in command {}:".format(ctx.command), file=sys.stderr
            )
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )


    ##################################################################################################
    ##################################################################################################
    ##################################################################################################

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"We have logged in as {self.bot.user}")

    @commands.command()
    async def shutdown(self, ctx: commands.Context):
        await ctx.send("Shutting down...")
        exit()

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
        aliases=["gitget"],
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
    async def delete(self, ctx: commands.Context, num: commands.Range[int, 0, 20] = 1):
        bot_msgs = [
            msg
            async for msg in ctx.channel.history(limit=20)
            if msg.author.id == self.bot.user.id
        ]

        await ctx.message.delete()

        def ordinal(x):
            return [
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

        for i in range(num):
            try:
                latest_message = bot_msgs.pop(0)
            except IndexError:
                latest_message = None

            if latest_message:
                await ctx.send(f"Deleting {ordinal(i)} latest message.", delete_after=2)
                await latest_message.delete()
            else:
                await ctx.send("Bot hasn't sent a message recently.", delete_after=2)
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
        banned_list = "```"
        banned_list += "\n".join(map(lambda id: ctx.guild.get_member(id).display_name, self.banned_set)) if self.banned_set else "No banned users yet."
        banned_list += "```"
        await ctx.send(banned_list)

async def setup(bot: commands.Bot):
    await bot.add_cog(DevelopersOnly(bot))
