import discord
from discord.ext import commands
import asyncio
import datetime


class noCategory(commands.Cog, name="No Category"):
    def __init__(self, bot, utils, filter_no_spam, robux, mysql_connection):
        self.bot = bot
        self.utils = utils
        self.filter_no_spam = filter_no_spam
        self.robux = robux
        self.mysql_connection = mysql_connection

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        emj = self.mysql_connection.get_emoji_icon(1)
        if (
            self.bot.get_user(payload.user_id) == self.bot.user
            or str(payload.emoji) != emj
        ):
            return

        async def points():
            channel = self.bot.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            ctx = await self.bot.get_context(msg)
            if (
                msg.content
                == f"{emj} oh! a wild robux appeared, use the reaction to win it!!"
                and msg.author == self.bot.user
            ):
                if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
                    return

                await msg.clear_reactions()
                await msg.edit(content=f"<@{payload.user_id}> you win!")
                try:
                    await self.robux.robux(ctx, str(payload.user_id), 1)
                except Exception:
                    await asyncio.sleep(10)
                    await self.robux.robux(ctx, str(payload.user_id), 1)

        try:
            await points()
        except Exception:
            await self.bot.get_channel(payload.channel_id).send(
                f"<@{payload.user_id}> sorry, something went wrong"
            )

    # PendingDeprecationWarning
    @commands.command()
    async def Embed(self, ctx, description, image):
        """⚠ This command is deprecated, instead use /embed ⚠
        you send an embed on Announcements Channel"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return

        if self.mysql_connection.is_exist(
            "guild_id", ctx.guild.id, "guilds", "announcementsChannel"
        ):
            prefix = self.mysql_connection.get_guild_data(ctx.guild.id, "prefix")
            await ctx.send(
                f"set an announcements channel, {prefix}setAnnouncementsChannel"
            )
            return

        channel = discord.utils.get(
            ctx.guild.text_channels,
            id=int(
                self.mysql_connection.get_guild_data(
                    ctx.guild.id, "announcementsChannel"
                )
            ),
        )
        embed = discord.Embed(
            description=description, timestamp=datetime.datetime.utcnow()
        )
        embed.set_image(url=image)

        await channel.send(embed=embed)


async def setup(bot, utils, filter_no_spam, robux, mysql_connection):
    await bot.add_cog(noCategory(bot, utils, filter_no_spam, robux, mysql_connection))
