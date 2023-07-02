import discord
from discord.ext import commands
from discord import app_commands

import asyncio
import datetime

from lib.utils import Utils
from lib.legacy_cog.noCategory import noCategory as LegacyNoCategory


class noCategory(LegacyNoCategory, name="No Category"):
    def __init__(self, bot, utils, filter_no_spam, robux, mysql_connection):
        super().__init__(bot, utils, filter_no_spam, robux, mysql_connection)

    @app_commands.command(
        name="embed",
        description="you send an embed on Announcements Channel",
    )
    @app_commands.describe(description="your text")
    @app_commands.describe(image="your image")
    async def Embed_slash(
        self,
        interaction: discord.Interaction,
        description: str,
        image: discord.Attachment,
    ):
        if await self.utils.is_ban(
            await Utils.getCtx(self.bot, interaction), self.filter_no_spam, self.robux
        ):
            return

        if self.mysql_connection.is_exist(
            "guild_id", interaction.guild_id, "guilds", "announcementsChannel"
        ):
            prefix = self.mysql_connection.get_guild_data(
                interaction.guild_id, "prefix"
            )
            await interaction.response.send_message(
                f"set an announcements channel, {prefix}setAnnouncementsChannel"
            )
            return

        channel = discord.utils.get(
            interaction.guild.text_channels,
            id=int(
                self.mysql_connection.get_guild_data(
                    interaction.guild_id, "announcementsChannel"
                )
            ),
        )
        embed = discord.Embed(
            description=description, timestamp=datetime.datetime.utcnow()
        )
        embed.set_image(url=image)

        await channel.send(embed=embed)
        await interaction.response.send_message("message sent")


async def setup(bot, utils, filter_no_spam, robux, mysql_connection):
    await bot.add_cog(noCategory(bot, utils, filter_no_spam, robux, mysql_connection))
