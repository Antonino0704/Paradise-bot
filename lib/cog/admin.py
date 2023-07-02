import discord
from discord.ext import commands
from discord import app_commands

import datetime

from lib.spam_lib import Spam
from lib.robux import Robux
from lib.inventory import Inventory
from lib.utils import Utils

from lib.legacy_cog.admin import Admin as LegacyAdmin


class Admin(LegacyAdmin, name="Owner"):
    def __init__(self, bot, filter_no_spam, robux, inventory, mysql_connection):
        super().__init__(bot, filter_no_spam, robux, inventory, mysql_connection)

    @app_commands.command(
        name="embed-admin", description="it sends embed to all bot's guilds"
    )
    @app_commands.describe(title="message title")
    @app_commands.describe(description="message description")
    @app_commands.describe(url_image="url of an image")
    async def embedAdmin_slash(
        self,
        interaction: discord.Interaction,
        title: str,
        description: str,
        url_image: str,
    ):
        ctx = await Utils.getCtx(self.bot, interaction)
        if await super().passAdminCheck(ctx):
            embed = discord.Embed(
                title=title,
                description=description,
                timestamp=datetime.datetime.utcnow(),
            )
            embed.set_image(url=url_image)
            embed.set_author(
                name=interaction.user.display_name,
                icon_url=interaction.user.avatar,
            )

            for guild in self.bot.guilds:
                await super().embed_admin_channel(embed, guild, 0)

    @app_commands.command(name="black-list", description="it adds user to blacklist")
    @app_commands.describe(id="user id")
    async def blackList_slash(self, interaction: discord.Interaction, id: str):
        ctx = await Utils.getCtx(self.bot, interaction)
        if await super().passAdminCheck(ctx):
            await self.filter_no_spam.add_black_list(ctx, id)

    @app_commands.command(
        name="remove-black-list", description="it removes user from blacklist"
    )
    @app_commands.describe(id="user id")
    async def removeBlackList_slash(self, interaction: discord.Interaction, id: str):
        ctx = await Utils.getCtx(self.bot, interaction)
        if await super().passAdminCheck(ctx):
            await self.filter_no_spam.remove_black_list(interaction, id)

    @app_commands.command(
        name="add-nowords", description="it adds word or words in prohibited words list"
    )
    @app_commands.describe(words="word or words that will be banned")
    async def addNoWords_slash(self, interaction: discord.Interaction, words: str):
        ctx = await Utils.getCtx(self.bot, interaction)
        if await super().passAdminCheck(ctx):
            words = words.replace("\n", " ")
            words = words.split(" ")
            await self.filter_no_spam.add_no_words(ctx, words)

    @app_commands.command(
        name="remove-nowords",
        description="it removes word or words from prohibited words list",
    )
    @app_commands.describe(words="word or words that will be unbanned")
    async def removeNoWords_slash(self, interaction: discord.Interaction, words: str):
        ctx = await Utils.getCtx(self.bot, interaction)
        if await super().passAdminCheck(ctx):
            words = words.replace("\n", " ")
            words = words.split(" ")
            await self.filter_no_spam.remove_no_words(ctx, words)

    @app_commands.command(
        name="money", description="it adds or removes robux from user"
    )
    @app_commands.describe(id="user id")
    @app_commands.describe(robux_number="number of robux to give")
    async def money(self, interaction: discord.Interaction, id: str, robux_number: int):
        ctx = await Utils.getCtx(self.bot, interaction)
        if await super().passAdminCheck(ctx):
            await self.robux.robux(ctx, id, robux_number)

    @app_commands.command(
        name="inventory",
        description="it adds or removes every type of item from inventory",
    )
    @app_commands.describe(id="user id")
    @app_commands.describe(type_object="type of inventory item")
    @app_commands.describe(number="number of items to be given")
    async def inventory_slash(
        self, interaction: discord.Interaction, id: str, type_object: str, number: int
    ):
        ctx = await Utils.getCtx(self.bot, interaction)
        if await super().passAdminCheck(ctx):
            await self.inventory.buy_object(ctx, id, type_object, number)

    @app_commands.command(
        name="get-robux-list",
        description="it sends the list of users who have the robux",
    )
    async def getRobuxList_slash(self, interaction: discord.Interaction):
        if await super().passAdminCheck(await Utils.getCtx(self.bot, interaction)):
            robux_list = self.mysql_connection.get_robux_list()
            description = ""
            for index in robux_list:
                description += f"<@{index[0]}> : {self.mysql_connection.get_emoji_icon(1)} {index[1]}\n"

                if len(description) > 3000 and len(description) < 4096:
                    embed = discord.Embed(
                        title="Robux user list", description=description
                    )
                    await interaction.response.send_message(embed=embed)
                    description = ""

            if description != None:
                embed = discord.Embed(title="Robux user list", description=description)
                await interaction.channel.send(embed=embed)
                await interaction.response.defer()

    @app_commands.command(
        name="add-badge",
        description="it adds badge to database",
    )
    @app_commands.describe(name="badge name")
    @app_commands.describe(emoji="emoji associated")
    @app_commands.describe(description="badge description")
    async def addBadge_slash(
        self,
        interaction: discord.Interaction,
        name: str,
        emoji: str,
        description: str = "no description",
    ):
        if await super().passAdminCheck(await Utils.getCtx(self.bot, interaction)):
            self.mysql_connection.add_badge(name, description, emoji)
            await interaction.response.send_message("badge activated")

    @app_commands.command(
        name="remove-badge",
        description="it removes badge from database",
    )
    @app_commands.describe(emoji="badge emoji")
    async def removeBadge_slash(self, interaction: discord.Interaction, emoji: str):
        if await super().passAdminCheck(await Utils.getCtx(self.bot, interaction)):
            badge_id = self.mysql_connection.get_badge_by_icon(emoji)
            if not self.mysql_connection.is_exist(
                "badge_id", badge_id, "badges", "badge_id"
            ):
                self.mysql_connection.remove_badges(badge_id)
                await interaction.response.send_message("badge disabled")
            else:
                await interaction.response.send_message("badge doesn't exist")

    @app_commands.command(
        name="add-badge-user",
        description="it adds badge to user",
    )
    @app_commands.describe(id="user id")
    @app_commands.describe(emoji="badge emoji")
    async def addBadgeUser_slash(
        self, interaction: discord.Interaction, id: str, emoji: str
    ):
        if await super().passAdminCheck(await Utils.getCtx(self.bot, interaction)):
            badge_id = self.mysql_connection.get_badge_by_icon(emoji)

            if not self.mysql_connection.is_exist_composite(
                "user_id", "badge_id", id, badge_id, "inventories", "received"
            ):
                await interaction.response.send_message(
                    f"<@{id}>, you already have the badge"
                )
                return

            if not self.mysql_connection.is_exist(
                "badge_id", badge_id, "badges", "badge_id"
            ):
                if self.mysql_connection.is_exist("user_id", id, "users", "user_id"):
                    self.mysql_connection.add_user(id)

                self.mysql_connection.add_badge_to_user(id, badge_id)
                await interaction.response.send_message(f"<@{id}> gets {emoji} badge")
            else:
                await interaction.response.send_message("badge doesn't exist")

    @app_commands.command(
        name="remove-badge-user",
        description="it removes badge to user",
    )
    @app_commands.describe(id="user id")
    @app_commands.describe(emoji="badge emoji")
    async def removeBadgeUser_slash(
        self, interaction: discord.Interaction, id: str, emoji: str
    ):
        if await super().passAdminCheck(await Utils.getCtx(self.bot, interaction)):
            badge_id = self.mysql_connection.get_badge_by_icon(emoji)

            if not self.mysql_connection.is_exist(
                "badge_id", badge_id, "badges", "badge_id"
            ):
                if not self.mysql_connection.is_exist_composite(
                    "user_id", "badge_id", id, badge_id, "inventories", "received"
                ):
                    self.mysql_connection.delete_badge_to_user(id, badge_id)
                    await interaction.response.send_message(
                        f"<@{id}> drops {emoji} badge"
                    )
                else:
                    await interaction.response.send_message(
                        f"<@{id}>, you don't have the badge"
                    )
            else:
                await interaction.response.send_message("badge doesn't exist")

    @app_commands.command(
        name="get-emoji",
        description="you get emoji like to string",
    )
    async def getEmoji_slash(self, interaction: discord.Interaction, emoji: str):
        if await super().passAdminCheck(await Utils.getCtx(self.bot, interaction)):
            emoji = emoji.replace("<", "")
            await interaction.response.send_message(emoji)

    @app_commands.command(
        name="responding",
        description="you send a message as bot",
    )
    @app_commands.describe(id_message="id of the message you want to reply to")
    @app_commands.describe(id_channel="id of channel where the message is located")
    @app_commands.describe(text="your text")
    async def responding_slash(
        self,
        interaction: discord.Interaction,
        id_message: str,
        id_channel: str,
        text: str,
    ):
        if await super().passAdminCheck(await Utils.getCtx(self.bot, interaction)):
            try:
                channel = self.bot.get_channel(int(id_channel))
                msg = await channel.fetch_message(id_message)
                ctx_msg = await self.bot.get_context(msg)
                await ctx_msg.reply(text)
            except:
                await interaction.response.send_message(
                    "error message or channel not found"
                )

    @app_commands.command(
        name="disconnect",
        description="disconnect from a specific guild",
    )
    @app_commands.describe(id_guild="id of the guild from where you want to disconnect")
    async def disconnect_slash(self, interaction: discord.Interaction, id_guild: str):
        if await super().passAdminCheck(await Utils.getCtx(self.bot, interaction)):
            try:
                guild = self.bot.get_guild(int(id_guild))
                voice = guild.voice_client
                await voice.disconnect()
            except:
                await interaction.response.send_message(
                    "error guild not found or already disconnected"
                )

    @app_commands.command(
        name="event",
        description="it starts an event",
    )
    @app_commands.describe(name="event name")
    @app_commands.describe(description="event description")
    @app_commands.describe(emoji="event badge")
    @app_commands.describe(finish_at="when the event finishes")
    @app_commands.describe(start="start number range obtaining")
    @app_commands.describe(end="end number range obtaining")
    @app_commands.describe(limit="max range 1 to limit")
    async def event(
        self,
        interaction: discord.Interaction,
        name: str,
        emoji: str,
        finish_at: str,
        start: int,
        end: int,
        limit: int,
        description: str = "No Description",
    ):
        if await super().passAdminCheck(await Utils.getCtx(self.bot, interaction)):
            badge_id = self.mysql_connection.get_badge_by_icon(emoji)

            if not self.mysql_connection.is_exist(
                "badge_id", badge_id, "badges", "badge_id"
            ):
                self.mysql_connection.add_event(
                    name,
                    description,
                    interaction.user.id,
                    badge_id,
                    finish_at,
                    start,
                    end,
                    limit,
                )
                await interaction.response.send_message(
                    f"<@{interaction.user.id}> created {emoji}{name} event"
                )
            else:
                await interaction.response.send_message("badge doesn't exist")

    @app_commands.command(
        name="add-item",
        description="it adds items to database",
    )
    @app_commands.describe(name="item name")
    @app_commands.describe(description="item description")
    @app_commands.describe(emoji="emoji associated")
    @app_commands.describe(price="item price")
    async def addItem(
        self,
        interaction: discord.Interaction,
        name: str,
        description: str,
        emoji: str,
        price: int,
    ):
        if await super().passAdminCheck(await Utils.getCtx(self.bot, interaction)):
            self.mysql_connection.add_item(name, description, emoji, price)
            await interaction.response.send_message("item added")

    @app_commands.command(
        name="remove-item",
        description="it removes item from database",
    )
    @app_commands.describe(emoji="item emoji")
    async def removeItem(self, interaction: discord.Interaction, emoji: str):
        if await super().passAdminCheck(await Utils.getCtx(self.bot, interaction)):
            item_id = self.mysql_connection.get_item_by_icon(emoji)
            if not self.mysql_connection.is_exist(
                "item_id", item_id, "items", "item_id"
            ):
                self.mysql_connection.remove_items(item_id)
                await interaction.response.send_message("item deleted")
            else:
                await interaction.response.send_message("item doesn't exist")

    @app_commands.command(
        name="item-user",
        description="it adds item to user",
    )
    @app_commands.describe(id="user id")
    @app_commands.describe(emoji="item emoji")
    @app_commands.describe(number="quantity")
    async def addItemUser(
        self, interaction: discord.Interaction, id: str, emoji: str, number: int
    ):
        if await super().passAdminCheck(await Utils.getCtx(self.bot, interaction)):
            item_id = self.mysql_connection.get_item_by_icon(emoji)

            if not self.mysql_connection.is_exist(
                "item_id", item_id, "items", "item_id"
            ):
                if self.mysql_connection.is_exist("user_id", id, "users", "user_id"):
                    self.mysql_connection.add_user(id)

                if self.mysql_connection.is_exist_composite(
                    "user_id", "item_id", id, item_id, "pokedex", "amount"
                ):
                    self.mysql_connection.add_item_to_user(id, item_id)

                amount = self.mysql_connection.get_pokedex(id, item_id)
                self.mysql_connection.update_pokedex(id, item_id, amount + number)
                await interaction.response.send_message(f"{number} {emoji} to <@{id}>")
            else:
                await interaction.response.send_message("item doesn't exist")


async def setup(bot, filter_no_spam, robux, inventory, mysql_connection):
    await bot.add_cog(Admin(bot, filter_no_spam, robux, inventory, mysql_connection))
