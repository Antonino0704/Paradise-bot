import json
import discord
from lib.spam_lib import Spam
from lib.robux import Robux
import re


class Utils:
    def __init__(self, mysql_connection):
        self.mysql_connection = mysql_connection

    def get_prefix(self, bot, msg):
        return self.mysql_connection.get_guild_data(msg.guild.id, "prefix")

    def mention_replace(self, mention_role):
        mention_role = mention_role.replace("<", "")
        mention_role = mention_role.replace("&", "")
        mention_role = mention_role.replace(">", "")
        mention_role = mention_role.replace("@", "")
        return mention_role

    async def is_ban(self, ctx, filter_no_spam, robux):
        if filter_no_spam.check_black_list(str(ctx.message.author.id)):
            if robux.less_one_robux(str(ctx.message.author.id)):
                await ctx.reply(f"-1 {self.mysql_connection.get_emoji_icon(1)}")

            await ctx.reply("you are banned")
            return True
        return False

    async def disconnection_for_inactivity(self, guild, n):
        channel_id = self.mysql_connection.get_guild_data(guild.id, "channel")
        if channel_id is not None:
            channel = discord.utils.get(guild.channels, id=int(channel_id))
            await channel.send("disconnection for inactivity")
            return
        try:
            channel = guild.text_channels[n]
            await channel.send("disconnection for inactivity")
        except:
            return await self.disconnection_for_inactivity(guild, n + 1)

    def gets_item_icon(self):
        icons = self.mysql_connection.get_all_emoji_icon()
        item_list = []
        for icon in icons:
            item_list.append(icon[0])
        return item_list

    @staticmethod
    async def getCtx(bot, interaction):
        return await bot.get_context(interaction)

    @staticmethod
    def remove_emoji(string):
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "\U0001f926-\U0001f937"
            "\U00010000-\U0010ffff"
            "\u200d"
            "\u2640-\u2642"
            "\u2600-\u2B55"
            "\u23cf"
            "\u23e9"
            "\u231a"
            "\u3030"
            "\ufe0f"
            "\u2069"
            "\u2066"
            "\u200c"
            "\u2068"
            "\u2067"
            "]+",
            flags=re.UNICODE,
        )
        return emoji_pattern.sub(r"", string)
