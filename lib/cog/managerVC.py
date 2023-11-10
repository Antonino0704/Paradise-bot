import discord
from discord.ext import commands
from discord import app_commands

import os
from gtts import gTTS
import asyncio
from pytube import YouTube
from pytube.exceptions import RegexMatchError

from lib.utils import Utils
from lib.spam_lib import Spam
from lib.robux import Robux
from lib.cog.events import Events

from lib.legacy_cog.managerVC import ManagerVC as LegacyManagerVC


class ManagerVC(LegacyManagerVC, name="Manager commands for bot's speech synthesis"):
    def __init__(
        self, bot, songs, ffmpeg, utils, filter_no_spam, robux, queue, mysql_connection
    ):
        super().__init__(
            bot, songs, ffmpeg, utils, filter_no_spam, robux, queue, mysql_connection
        )

    @app_commands.command(
        name="left",
        description="the bot leaves the channel",
    )
    async def left_slash(self, interaction: discord.Interaction):
        if await self.utils.is_ban(
            await Utils.getCtx(self.bot, interaction), self.filter_no_spam, self.robux
        ):
            return
        try:
            voice = interaction.guild.voice_client
            await voice.disconnect()
            await interaction.response.send_message("I disconnected", ephemeral=True)
        except:
            await interaction.response.send_message(
                "you are not connected to a voice channel"
            )

    @app_commands.command(
        name="leave",
        description="alternative command for left, the bot leaves the channel",
    )
    async def leave_slash(self, interaction: discord.Interaction):
        if await self.utils.is_ban(
            await Utils.getCtx(self.bot, interaction), self.filter_no_spam, self.robux
        ):
            return
        try:
            voice = interaction.guild.voice_client
            await voice.disconnect()
            await interaction.response.send_message("I disconnected", ephemeral=True)
        except:
            await interaction.response.send_message(
                "you are not connected to a voice channel"
            )

    @app_commands.command(
        name="stop",
        description="the bot stops",
    )
    async def stop_slash(self, interaction: discord.Interaction):
        if await self.utils.is_ban(
            await Utils.getCtx(self.bot, interaction), self.filter_no_spam, self.robux
        ):
            return

        for index in range(0, len(self.queue[interaction.guild.id]["content"])):
            if index != 0:
                del self.queue[interaction.guild.id]["content"][index]
        voice = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        voice.stop()
        await interaction.response.send_message("I stopped", ephemeral=True)

    @app_commands.command(
        name="skip",
        description="the bot skips song",
    )
    async def skip_slash(self, interaction: discord.Interaction):
        if await self.utils.is_ban(
            await Utils.getCtx(self.bot, interaction), self.filter_no_spam, self.robux
        ):
            return
        voice = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        voice.stop()
        await interaction.response.send_message("I skipped", ephemeral=True)

    @app_commands.command(
        name="spam",
        description="if no the spam filter will be activate",
    )
    @app_commands.choices(
        spam=[
            app_commands.Choice(name="Yes", value="yes"),
            app_commands.Choice(name="No", value="no"),
        ]
    )
    @app_commands.describe(spam="value boolean")
    async def spam(self, interaction: discord.Interaction, spam: str):
        if await self.utils.is_ban(
            await Utils.getCtx(self.bot, interaction), self.filter_no_spam, self.robux
        ):
            return

        self.mysql_connection.update_guild_data(interaction.guild_id, "spam", spam)
        await interaction.response.send_message("spam has been set")
