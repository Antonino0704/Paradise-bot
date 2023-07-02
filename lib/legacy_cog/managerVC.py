import discord
from discord.ext import commands

import json
from json.decoder import JSONDecodeError
import os
from gtts import gTTS
import asyncio
from pytube import YouTube
from pytube.exceptions import RegexMatchError

from lib.utils import Utils
from lib.spam_lib import Spam
from lib.robux import Robux
from lib.cog.events import Events


class ManagerVC(commands.Cog, name="Manager commands for bot's speech synthesis"):
    def __init__(
        self, bot, songs, ffmpeg, utils, filter_no_spam, robux, queue, mysql_connection
    ):
        self.bot = bot
        self.songs = songs
        self.ffmpeg = ffmpeg
        self.utils = utils
        self.filter_no_spam = filter_no_spam
        self.robux = robux
        self.queue = queue
        self.mysql_connection = mysql_connection

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.id == self.bot.user.id:
            return

        elif before.channel is None:
            voice = after.channel.guild.voice_client
            time = 0
            while True:
                await asyncio.sleep(1)
                time = time + 1
                if voice.is_playing() and not voice.is_paused():
                    time = 0
                if time >= 600:
                    await voice.disconnect()
                    await self.utils.disconnection_for_inactivity(
                        after.channel.guild, 0
                    )
                if not voice.is_connected():
                    break

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.bot.user:
            return
        try:
            data = self.mysql_connection.get_guild_data_managerVC(
                msg.guild.id, "prefix, prefixVC, channel"
            )[0]
            if msg.content[0] != data[0]:
                if msg.content[0] == data[1]:
                    await self.prefixMethods(msg)
                    return
                if str(msg.channel.id) == data[2]:
                    await self.prefixMethods(msg)
        except IndexError:
            pass

    async def prefixMethods(self, msg):
        ctx = await self.bot.get_context(msg)
        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return

        self.queue[msg.guild.name]["content"].append(msg.content)
        self.filter_no_spam.msg_stopped = len(msg.content)
        await self.events(ctx)
        print(len(self.queue[msg.guild.name]["content"]))
        if len(self.queue[msg.guild.name]["content"]) == 1:
            await self.speak(msg)

    async def events(self, ctx):
        await self.robux.catch(ctx)
        events = self.mysql_connection.get_events()
        if events:
            for event in events:
                await Events.event_message(
                    ctx, event[0], event[1], event[2], event[3], event[4]
                )

    def finish(self, msg):
        try:
            del self.queue[msg.guild.name]["content"][0]
            self.queue[msg.guild.name]["status"] = False
        except IndexError:
            print("index error")

    async def speak(self, msg):
        data = self.mysql_connection.get_guild_data_managerVC(
            msg.guild.id, "spam, lang"
        )[0]

        while len(self.queue[msg.guild.name]["content"]) != 0:
            try:
                if os.path.exists(msg.guild.name + ".mp3"):
                    os.remove(msg.guild.name + ".mp3")

                path = self.songs
                if (
                    self.queue[msg.guild.name]["content"][0][1:25]
                    != "https://www.youtube.com/"
                    and self.queue[msg.guild.name]["content"][0][1:24]
                    != "ttps://www.youtube.com/"
                ):
                    if data[0] == "no":
                        self.queue[msg.guild.name]["content"][
                            0
                        ] = self.filter_no_spam.censured(
                            self.queue[msg.guild.name]["content"][0]
                        )

                    tts = gTTS(
                        self.queue[msg.guild.name]["content"][0],
                        lang=data[1],
                        slow=False,
                    )
                    tts.save(f"{path}/{msg.guild.name}.mp3")

                else:
                    # not work
                    YouTube(
                        self.queue[msg.guild.name]["content"][0][1:]
                    ).streams.filter(only_audio=True).first().download(
                        path, filename=msg.guild.name + ".mp3"
                    )
                if not msg.guild.voice_client in self.bot.voice_clients:
                    channel = msg.author.voice.channel
                    await channel.connect()

                voice = discord.utils.get(self.bot.voice_clients, guild=msg.guild)
                self.queue[msg.guild.name]["status"] = True
                voice.play(
                    discord.FFmpegPCMAudio(
                        executable=self.ffmpeg, source=path + msg.guild.name + ".mp3"
                    ),
                    after=lambda e: self.finish(msg),
                )

                while self.queue[msg.guild.name]["status"]:
                    await asyncio.sleep(1)

            except AttributeError:
                await msg.channel.send(
                    "you are not connected to a voice channel", reference=msg
                )
                self.finish(msg)

            except ValueError:
                await msg.channel.send(
                    "language you have selected doesn't exist, please change it",
                    reference=msg,
                )
                self.finish(msg)

            except RegexMatchError:
                await msg.channel.send("video not found", reference=msg)
                self.finish(msg)

    # PendingDeprecationWarning
    @commands.command()
    async def left(self, ctx):
        """⚠ This command is deprecated, instead use /left ⚠
        the bot leaves the channel"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        try:
            voice = ctx.guild.voice_client
            await voice.disconnect()
        except:
            await ctx.reply("you are not connected to a voice channel")

    # PendingDeprecationWarning
    @commands.command()
    async def leave(self, ctx):
        """⚠ This command is deprecated, instead use /leave ⚠
        alternative command for left, the bot leaves the channel"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        try:
            voice = ctx.guild.voice_client
            await voice.disconnect()
        except:
            await ctx.reply("you are not connected to a voice channel")

    # PendingDeprecationWarning
    @commands.command()
    async def stop(self, ctx):
        """⚠ This command is deprecated, instead use /stop ⚠
        the bot stops"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return

        for index in range(0, len(self.queue[ctx.guild.name]["content"])):
            if index != 0:
                del self.queue[ctx.guild.name]["content"][index]
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()

    # PendingDeprecationWarning
    @commands.command()
    async def skip(self, ctx):
        """⚠ This command is deprecated, instead use /skip ⚠
        the bot skips song"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()

    # PendingDeprecationWarning
    @commands.command()
    async def spam(self, ctx, spam):
        """⚠ This command is deprecated, instead use /spam ⚠
        use only yes or no, if no the spam filter will be activate"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return

        if spam != "yes" and spam != "no":
            await ctx.reply("use only yes or no")
            return

        self.mysql_connection.update_guild_data(ctx.guild.id, "spam", spam)
        await ctx.send("spam has been set")

    # for the unconnected bug, read readme.md
    @commands.command(hidden=True)
    async def clean(self, ctx):
        try:
            for index in range(0, len(self.queue[ctx.guild.name]["content"])):
                del self.queue[ctx.guild.name]["content"][index]
        except:
            pass
