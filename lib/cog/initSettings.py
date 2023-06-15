import discord
from discord.ext import commands
from discord import app_commands

import typing

from lib.utils import Utils
from lib.spam_lib import Spam
from lib.robux import Robux

from lib.legacy_cog.initSettings import InitSettings as LegacyInitSettings


class InitSettings(LegacyInitSettings, name="Initializing bot settings"):
    def __init__(self, bot, utils, filter_no_spam, robux, mysql_connection):
        super().__init__(bot, utils, filter_no_spam, robux, mysql_connection)

    @app_commands.command(
        name="set-channel",
        description="it sets the channel in which all messages are read by the bot",
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.describe(channel="the channel")
    async def setChannel_slash(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        try:
            if await self.utils.is_ban(
                await Utils.getCtx(self.bot, interaction),
                self.filter_no_spam,
                self.robux,
            ):
                return

            self.mysql_connection.update_guild_data(
                interaction.guild_id, "channel", channel.id
            )
            await interaction.response.send_message(
                "the channel has been set", ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(e)

    @app_commands.command(
        name="remove-channel",
        description="it removes the channel in which all messages are read by the bot",
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.default_permissions(manage_guild=True)
    async def removeChannel_slash(self, interaction: discord.Interaction):
        if await self.utils.is_ban(
            await Utils.getCtx(self.bot, interaction), self.filter_no_spam, self.robux
        ):
            return

        if not self.mysql_connection.is_exist(
            "guild_id", interaction.guild_id, "guilds", "channel"
        ):
            try:
                self.mysql_connection.update_guild_data(
                    interaction.guild_id, "channel", None
                )
                await interaction.response.send_message(
                    "the channel has been removed", ephemeral=True
                )
            except Exception as e:
                await interaction.response.send_message(e, ephemeral=True)

        else:
            await interaction.response.send_message(
                "you don't have a channel", ephemeral=True
            )

    @app_commands.command(
        name="set-announcements-channel",
        description="it sets the channel in which the embed command sends the messages",
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.describe(channel="the channel")
    async def setAnnouncementsChannel_slash(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        try:
            if await self.utils.is_ban(
                await Utils.getCtx(self.bot, interaction),
                self.filter_no_spam,
                self.robux,
            ):
                return

            self.mysql_connection.update_guild_data(
                interaction.guild_id, "announcementsChannel", channel.id
            )
            await interaction.response.send_message(
                "channel has been set", ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(e, ephemeral=True)

    @app_commands.command(
        name="remove-announcements-channel",
        description="it removes the channel in which the embed command sends the messages",
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.default_permissions(manage_guild=True)
    async def removeAnnouncementsChannel_slash(self, interaction: discord.Interaction):
        if await self.utils.is_ban(
            await Utils.getCtx(self.bot, interaction), self.filter_no_spam, self.robux
        ):
            return

        if not self.mysql_connection.is_exist(
            "guild_id", interaction.guild_id, "guilds", "announcementsChannel"
        ):
            try:
                self.mysql_connection.update_guild_data(
                    interaction.guild_id, "announcementsChannel", None
                )
                await interaction.response.send_message(
                    "channel has been removed", ephemeral=True
                )
            except Exception as e:
                await interaction.response.send_message(e, ephemeral=True)

        else:
            await interaction.response.send_message(
                "you don't have a channel", ephemeral=True
            )

    @app_commands.command(
        name="prefix-vc",
        description="it sets the prefix for the messages that are read by the bot",
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.describe(prefixvc="the prefix vc")
    async def setPrefixVC_slash(self, interaction: discord.Interaction, prefixvc: str):
        if await self.utils.is_ban(
            await Utils.getCtx(self.bot, interaction), self.filter_no_spam, self.robux
        ):
            return

        self.mysql_connection.update_guild_data(
            interaction.guild_id, "prefixVC", prefixvc
        )
        await interaction.response.send_message(
            "prefix vocal has been set", ephemeral=True
        )

    @app_commands.command(
        name="remove-prefix-vc",
        description="it removes the prefix for the messages the are read by the bot",
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.default_permissions(manage_guild=True)
    async def removePrefixVC_slash(self, interaction: discord.Interaction):
        if await self.utils.is_ban(
            await Utils.getCtx(self.bot, interaction), self.filter_no_spam, self.robux
        ):
            return

        if not self.mysql_connection.is_exist(
            "guild_id", interaction.guild_id, "guilds", "prefixVC"
        ):
            self.mysql_connection.update_guild_data(
                interaction.guild_id, "prefixVC", None
            )
            await interaction.response.send_message(
                "prefix vocal has been deleted", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "you don't have a prefixVC", ephemeral=True
            )

    async def tts_langs(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> typing.List[app_commands.Choice[str]]:
        choices = [
            "af",
            "ar",
            "bg",
            "bn",
            "bs",
            "ca",
            "cs",
            "cy",
            "da",
            "de",
            "el",
            "en",
            "eo",
            "es",
            "et",
            "fi",
            "fr",
            "gu",
            "hi",
            "hr",
            "hu",
            "hy",
            "is",
            "it",
            "ja",
        ]
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices
            if current.lower() in choice.lower()
        ]

    @app_commands.command(name="set-lang", description="it sets iso language code")
    @app_commands.autocomplete(new_lang=tts_langs)
    async def setLang_slash(self, interaction: discord.Interaction, new_lang: str):
        if await self.utils.is_ban(
            await Utils.getCtx(self.bot, interaction), self.filter_no_spam, self.robux
        ):
            return

        self.mysql_connection.update_guild_data(interaction.guild_id, "lang", new_lang)
        await interaction.response.send_message("new lang was set")

    @app_commands.command(
        name="set-first-last-name",
        description="it set your account's firstname and lastname",
    )
    @app_commands.describe(first_name="your first name")
    @app_commands.describe(last_name="tyour last name")
    async def setFirstLastName_slash(
        self, interaction: discord.Interaction, first_name: str, last_name: str
    ):
        if await self.utils.is_ban(
            await Utils.getCtx(self.bot, interaction), self.filter_no_spam, self.robux
        ):
            return
        id = str(interaction.user.id)

        if self.mysql_connection.is_exist("user_id", id, "users", "user_id"):
            self.mysql_connection.add_user(id)
        self.mysql_connection.update_user_names(id, first_name, last_name)
        await interaction.response.send_message(
            "firstname and lastname was set", ephemeral=True
        )


async def setup(bot, utils, filter_no_spam, robux, mysql_connection):
    await bot.add_cog(InitSettings(bot, utils, filter_no_spam, robux, mysql_connection))
