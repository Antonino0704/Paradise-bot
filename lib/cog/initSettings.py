import discord
from discord.ext import commands

import json

from lib.utils import Utils
from lib.spam_lib import Spam
from lib.robux import Robux


class InitSettings(commands.Cog, name="Initializing bot settings"):
    def __init__(self, bot, utils, filter_no_spam, robux, mysql_connection):
        self.bot = bot
        self.utils = utils
        self.filter_no_spam = filter_no_spam
        self.robux = robux
        self.mysql_connection = mysql_connection

    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def changePrefix(self, ctx, new_prefix):
        """it changes the bot prefix"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return

        self.mysql_connection.update_guild_data(ctx.guild.id, "prefix", new_prefix)
        await ctx.send("new prefix sets")

    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def setChannel(self, ctx, name_channel):
        """it sets the channel in which all messages are read by the bot"""

        channel = discord.utils.get(ctx.guild.text_channels, name=name_channel)

        try:
            if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
                return

            if channel is None:
                channel = await ctx.guild.create_text_channel(name_channel)

            self.mysql_connection.update_guild_data(ctx.guild.id, "channel", channel.id)
            await ctx.send("the channel has been set")
        except Exception as e:
            await ctx.reply(e)

    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def removeChannel(self, ctx):
        """it removes the channel in which all messages are read by the bot"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return

        if not self.mysql_connection.is_exist(
            "guild_id", ctx.guild.id, "guilds", "channel"
        ):
            try:
                channel_id = self.mysql_connection.get_guild_data(
                    ctx.guild.id, "channel"
                )
                channel = discord.utils.get(ctx.guild.text_channels, id=int(channel_id))
                await channel.delete()
                self.mysql_connection.update_guild_data(ctx.guild.id, "channel", None)
                await ctx.send("the channel has been deleted")
            except Exception as e:
                await ctx.reply(e)

        else:
            await ctx.send("you don't have a channel")

    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def setAnnouncementsChannel(self, ctx, name_channel):
        """it sets the channel in which the embed command sends the messages"""

        channel = discord.utils.get(ctx.guild.text_channels, name=name_channel)

        try:
            if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
                return

            if channel is None:
                channel = await ctx.guild.create_text_channel(name_channel)

            self.mysql_connection.update_guild_data(
                ctx.guild.id, "announcementsChannel", channel.id
            )
            await ctx.send("channel has been set")
        except Exception as e:
            await ctx.reply(e)

    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def removeAnnouncementsChannel(self, ctx):
        """it removes the channel in which the embed command sends the messages"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return

        if not self.mysql_connection.is_exist(
            "guild_id", ctx.guild.id, "guilds", "announcementsChannel"
        ):
            try:
                channel_id = self.mysql_connection.get_guild_data(
                    ctx.guild.id, "announcementsChannel"
                )
                channel = discord.utils.get(ctx.guild.text_channels, id=int(channel_id))

                if channel is None:
                    await ctx.reply("the channel doesn't exist")
                    return

                await channel.delete()
                self.mysql_connection.update_guild_data(
                    ctx.guild.id, "announcementsChannel", None
                )
                await ctx.send("channel has been deleted")
            except Exception as e:
                await ctx.reply(e)

        else:
            await ctx.send("you don't have a channel")

    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def setPrefixVC(self, ctx, prefixVC):
        """it sets the prefix for the messages that are read by the bot"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return

        self.mysql_connection.update_guild_data(ctx.guild.id, "prefixVC", prefixVC)
        await ctx.send("prefix vocal has been set")

    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def removePrefixVC(self, ctx):
        """it removes the prefix for the messages the are read by the bot"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return

        if not self.mysql_connection.is_exist(
            "guild_id", ctx.guild.id, "guilds", "prefixVC"
        ):
            self.mysql_connection.update_guild_data(ctx.guild.id, "prefixVC", None)
            await ctx.send("prefix vocal has been deleted")
        else:
            await ctx.send("you don't have a prefixVC")

    @commands.command()
    async def setLang(self, ctx, new_lang):
        """it sets iso language code"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return

        self.mysql_connection.update_guild_data(ctx.guild.id, "lang", new_lang)
        await ctx.send("new lang was set")

    @commands.command()
    async def setFirstLastName(self, ctx, firstName, lastName):
        """it set your account's firstname and lastname"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        id = str(ctx.message.author.id)
        if self.mysql_connection.is_exist("user_id", id, "users", "user_id"):
            self.mysql_connection.add_user(id)
        self.mysql_connection.update_user_names(id, firstName, lastName)
        await ctx.send("firstname and lastname was set")


async def setup(bot, utils, filter_no_spam, robux, mysql_connection):
    await bot.add_cog(InitSettings(bot, utils, filter_no_spam, robux, mysql_connection))
