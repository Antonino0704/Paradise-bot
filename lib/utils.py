import json
import discord
from lib.spam_lib import Spam
from lib.robux import Robux


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
