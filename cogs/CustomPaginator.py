from __future__ import annotations

import logging

import boto3
import discord
from discord.ext import commands


class Simple(discord.ui.View):
    """
    Embed Paginator.

    Parameters:
    ----------
    timeout: int
        How long the Paginator should timeout in, after the last interaction. (In seconds) (Overrides default of 60)
    PreviousButton: discord.ui.Button
        Overrides default previous button.
    NextButton: discord.ui.Button
        Overrides default next button.
    PageCounterStyle: discord.ButtonStyle
        Overrides default page counter style.
    InitialPage: int
        Page to start the pagination on.
    """

    def __init__(
        self,
        *,
        timeout: int = 60,
        PreviousButton: discord.ui.Button = discord.ui.Button(
            emoji=discord.PartialEmoji(name="\U000025c0")
        ),
        NextButton: discord.ui.Button = discord.ui.Button(
            emoji=discord.PartialEmoji(name="\U000025b6")
        ),
        PageCounterStyle: discord.ButtonStyle = discord.ButtonStyle.grey,
        InitialPage: int = 0,
        ephemeral: bool = False,
    ) -> None:
        self.PreviousButton = PreviousButton
        self.NextButton = NextButton
        self.PageCounterStyle = PageCounterStyle
        self.InitialPage = InitialPage
        self.ephemeral = ephemeral

        self.pages = None
        self.ctx = None
        self.message = None
        self.current_page = None
        self.page_counter = None
        self.total_page_count = None

        self.s3 = boto3.client("s3")
        self.bucket = "discordbotpics"
        self.logger = logging.getLogger("discord")

        super().__init__(timeout=timeout)

    async def start(
        self,
        ctx: discord.Interaction | commands.Context,
        pages: list[tuple[discord.Embed, str]],
    ):
        if isinstance(ctx, discord.Interaction):
            ctx = await commands.Context.from_interaction(ctx)

        self.pages = pages
        self.total_page_count = len(pages)
        self.ctx = ctx
        self.current_page = self.InitialPage

        self.PreviousButton.callback = self.previous_button_callback
        self.NextButton.callback = self.next_button_callback

        self.page_counter = SimplePaginatorPageCounter(
            style=self.PageCounterStyle,
            TotalPages=self.total_page_count,
            InitialPage=self.InitialPage,
        )

        self.add_item(self.PreviousButton)
        self.add_item(self.page_counter)
        self.add_item(self.NextButton)

        self.message = await ctx.send(
            embed=self.build_embed(self.pages[self.InitialPage]),
            view=self,
            ephemeral=self.ephemeral,
        )

    async def previous(self):
        if self.current_page == 0:
            self.current_page = self.total_page_count - 1
        else:
            self.current_page -= 1

        self.page_counter.label = f"{self.current_page + 1}/{self.total_page_count}"

        await self.message.edit(
            embed=self.build_embed(self.pages[self.current_page]), view=self
        )

    async def next(self):
        if self.current_page == self.total_page_count - 1:
            self.current_page = 0
        else:
            self.current_page += 1

        self.page_counter.label = f"{self.current_page + 1}/{self.total_page_count}"

        await self.message.edit(
            embed=self.build_embed(self.pages[self.current_page]), view=self
        )

    def build_embed(self, elem: tuple[discord.Embed, str]):
        self.logger.info(f"Building embed for {elem[1]}")
        embed = elem[0]
        url = self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": elem[1]},
            ExpiresIn=60,
        )
        embed.set_image(url=url)
        return embed

    async def next_button_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            embed = discord.Embed(
                description="You cannot control this pagination because you did not execute it.",
                color=discord.Colour.red(),
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.next()
        await interaction.response.defer()

    async def previous_button_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            embed = discord.Embed(
                description="You cannot control this pagination because you did not execute it.",
                color=discord.Colour.red(),
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.previous()
        await interaction.response.defer()


class SimplePaginatorPageCounter(discord.ui.Button):
    def __init__(self, style: discord.ButtonStyle, TotalPages, InitialPage):
        super().__init__(
            label=f"{InitialPage + 1}/{TotalPages}", style=style, disabled=True
        )
