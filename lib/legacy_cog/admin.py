import discord
from discord.ext import commands

import datetime
import json

from lib.spam_lib import Spam
from lib.robux import Robux
from lib.inventory import Inventory


class Admin(commands.Cog, name="Owner"):
    def __init__(self, bot, filter_no_spam, robux, inventory, mysql_connection):
        self.bot = bot
        self.filter_no_spam = filter_no_spam
        self.robux = robux
        self.inventory = inventory
        self.mysql_connection = mysql_connection

    async def passAdminCheck(self, ctx):
        ADMIN_PRIVILEGE = self.mysql_connection.check_privileges(
            str(ctx.message.author.id), 7
        )
        if not ADMIN_PRIVILEGE:
            await ctx.reply("You don't have permission to use this command")
            return False
        return True

    # PendingDeprecationWarning
    @commands.command()
    async def embedAdmin(self, ctx, title, description, url_image):
        """⚠ This command is deprecated, instead use /embed-admin ⚠
        it sends embed to all bot's guilds"""

        if await self.passAdminCheck(ctx):
            embed = discord.Embed(
                title=title,
                description=description,
                timestamp=datetime.datetime.utcnow(),
            )
            embed.set_image(url=url_image)
            embed.set_author(
                name=ctx.message.author, icon_url=ctx.message.author.avatar
            )
            for guild in self.bot.guilds:
                await self.embed_admin_channel(embed, guild, 0)

    async def embed_admin_channel(self, embed, guild, n):
        try:
            channel = guild.text_channels[n]
            await channel.send(embed=embed)
        except:
            return await self.embed_admin_channel(embed, guild, n + 1)

    # PendingDeprecationWarning
    @commands.command()
    async def blackList(self, ctx, id):
        """⚠ This command is deprecated, instead use /black-list ⚠
        it adds user to blacklist"""

        if await self.passAdminCheck(ctx):
            await self.filter_no_spam.add_black_list(ctx, id)

    # PendingDeprecationWarning
    @commands.command()
    async def removeBlackList(self, ctx, id):
        """⚠ This command is deprecated, instead use /remove-black-list ⚠
        it removes user from blacklist"""

        if await self.passAdminCheck(ctx):
            await self.filter_no_spam.remove_black_list(ctx, id)

    # PendingDeprecationWarning
    @commands.command()
    async def addNoWords(self, ctx, *, words):
        """⚠ This command is deprecated, instead use /add-nowords ⚠
        it adds word or words in prohibited words list"""

        if await self.passAdminCheck(ctx):
            words = words.replace("\n", " ")
            words = words.split(" ")
            await self.filter_no_spam.add_no_words(ctx, words)

    # PendingDeprecationWarning
    @commands.command()
    async def removeNoWords(self, ctx, *, words):
        """⚠ This command is deprecated, instead use /remove-nowords ⚠
        it removes word or words from prohibited words list"""

        if await self.passAdminCheck(ctx):
            words = words.replace("\n", " ")
            words = words.split(" ")
            await self.filter_no_spam.remove_no_words(ctx, words)

    # PendingDeprecationWarning
    @commands.command()
    async def money(self, ctx, id, robux_number):
        """⚠ This command is deprecated, instead use /money ⚠
        it adds or removes robux from user"""

        if await self.passAdminCheck(ctx):
            robux_number = int(robux_number)
            await self.robux.robux(ctx, id, robux_number)

    # PendingDeprecationWarning
    @commands.command()
    async def inventory(self, ctx, id, type_object, number):
        """⚠ This command is deprecated, instead use /inventory ⚠
        it adds or removes every type of item from inventory"""

        if await self.passAdminCheck(ctx):
            number = int(number)
            await self.inventory.buy_object(ctx, id, type_object, number)

    # PendingDeprecationWarning
    @commands.command()
    async def getRobuxList(self, ctx):
        """⚠ This command is deprecated, instead use /get-robux-list ⚠
        it sends the list of users who have the robux"""

        if await self.passAdminCheck(ctx):
            robux_list = self.mysql_connection.get_robux_list()
            description = ""
            for index in robux_list:
                description += f"<@{index[0]}> : {self.mysql_connection.get_emoji_icon(1)} {index[1]}\n"

                if len(description) > 3000 and len(description) < 4096:
                    embed = discord.Embed(
                        title="Robux user list", description=description
                    )
                    await ctx.send(embed=embed)
                    description = ""

            if description != None:
                embed = discord.Embed(title="Robux user list", description=description)
                await ctx.send(embed=embed)

    # PendingDeprecationWarning
    @commands.command()
    async def addBadge(self, ctx, name, emoji, description="no description"):
        """⚠ This command is deprecated, instead use /add-badge ⚠
        it adds badge to database"""

        if await self.passAdminCheck(ctx):
            self.mysql_connection.add_badge(name, description, emoji)
            await ctx.reply("badge activated")

    # PendingDeprecationWarning
    @commands.command()
    async def removeBadge(self, ctx, emoji):
        """⚠ This command is deprecated, instead use /remove-badge ⚠
        it removes badge from database"""

        if await self.passAdminCheck(ctx):
            badge_id = self.mysql_connection.get_badge_by_icon(emoji)
            if not self.mysql_connection.is_exist(
                "badge_id", badge_id, "badges", "badge_id"
            ):
                self.mysql_connection.remove_badges(badge_id)
                await ctx.reply("badge disabled")
            else:
                await ctx.reply("badge doesn't exist")

    # PendingDeprecationWarning
    @commands.command()
    async def addBadgeUser(self, ctx, id, emoji):
        """⚠ This command is deprecated, instead use /add-badge-user ⚠
        it adds badge to user"""

        if await self.passAdminCheck(ctx):
            badge_id = self.mysql_connection.get_badge_by_icon(emoji)

            if not self.mysql_connection.is_exist_composite(
                "user_id", "badge_id", id, badge_id, "inventories", "received"
            ):
                await ctx.reply(f"<@{id}>, you already have the badge")
                return

            if not self.mysql_connection.is_exist(
                "badge_id", badge_id, "badges", "badge_id"
            ):
                if self.mysql_connection.is_exist("user_id", id, "users", "user_id"):
                    self.mysql_connection.add_user(id)

                self.mysql_connection.add_badge_to_user(id, badge_id)
                await ctx.reply(f"<@{id}> gets {emoji} badge")
            else:
                await ctx.reply("badge doesn't exist")

    # PendingDeprecationWarning
    @commands.command()
    async def removeBadgeUser(self, ctx, id, emoji):
        """⚠ This command is deprecated, instead use /remove-badge-user ⚠
        it removes badge to user"""

        if await self.passAdminCheck(ctx):
            badge_id = self.mysql_connection.get_badge_by_icon(emoji)

            if not self.mysql_connection.is_exist(
                "badge_id", badge_id, "badges", "badge_id"
            ):
                if not self.mysql_connection.is_exist_composite(
                    "user_id", "badge_id", id, badge_id, "inventories", "received"
                ):
                    self.mysql_connection.delete_badge_to_user(id, badge_id)
                    await ctx.reply(f"<@{id}> drops {emoji} badge")
                else:
                    await ctx.reply(f"<@{id}>, you don't have the badge")
            else:
                await ctx.reply("badge doesn't exist")

    # PendingDeprecationWarning
    @commands.command()
    async def getEmoji(self, ctx, msg):
        """⚠ This command is deprecated, instead use /get-emoji ⚠
        you get emoji like to string"""

        if await self.passAdminCheck(ctx):
            msg = msg.replace("<", "")
            await ctx.reply(msg)

    # PendingDeprecationWarning
    @commands.command()
    async def responding(self, ctx, id_message, id_channel, text):
        """⚠ This command is deprecated, instead use /responding ⚠
        you send a message as bot"""

        if await self.passAdminCheck(ctx):
            try:
                channel = self.bot.get_channel(int(id_channel))
                msg = await channel.fetch_message(id_message)
                ctx_msg = await self.bot.get_context(msg)
                await ctx_msg.reply(text)
            except:
                await ctx.reply("error message or channel not found")

    # PendingDeprecationWarning
    @commands.command()
    async def disconnect(self, ctx, id_guild):
        """⚠ This command is deprecated, instead use /disconnect ⚠
        disconnect from a specific guild"""

        if await self.passAdminCheck(ctx):
            try:
                guild = self.bot.get_guild(int(id_guild))
                voice = guild.voice_client
                await voice.disconnect()
            except:
                await ctx.reply("error guild not found or already disconnected")


async def setup(bot, filter_no_spam, robux, inventory, mysql_connection):
    await bot.add_cog(Admin(bot, filter_no_spam, robux, inventory, mysql_connection))
