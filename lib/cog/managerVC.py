import discord
from discord.ext import commands

import json

from lib.utils import Utils
from lib.spam_lib import Spam
from lib.robux import Robux

class ManagerVC(commands.Cog, name="Manager commands for bot's speech synthesis"):
    def __init__(self, bot, utils, filter_no_spam, robux, database):
        self.bot = bot
        self.utils = utils
        self.filter_no_spam = filter_no_spam
        self.robux = robux
        self.database = database

    @commands.command()
    async def left(self, ctx):
        """the bot left channel"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        try:
            voice = ctx.guild.voice_client
            await voice.disconnect()
        except:
            await ctx.reply("you are not connected to a voice channel")
            
            

    @commands.command()
    async def stop(self, ctx):
        """the bot stops"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()
        

    @commands.command()
    async def spam(self, ctx, spam):
        """use only yes or no, if no the spam filter will be activate"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        
        if spam != "yes" and spam != "no":
            await ctx.reply("use only yes or no")
            return
        
        data = json.load(open(self.database))
        with open(self.database, 'w') as db:
            data[ctx.guild.name]["spam"] = spam
            json.dump(data, db)
            
        await ctx.send("spam set")