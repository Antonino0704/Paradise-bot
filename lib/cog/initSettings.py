import discord
from discord.ext import commands

import json

from lib.utils import Utils
from lib.spam_lib import Spam
from lib.robux import Robux

class InitSettings(commands.Cog, name="Initializing bot settings"):
    def __init__(self, bot, utils, filter_no_spam, robux, database):
        self.bot = bot
        self.utils = utils
        self.filter_no_spam = filter_no_spam
        self.robux = robux
        self.database = database

    @commands.command()
    async def changePrefix(self, ctx, new_prefix):
        """change prefix of bot"""

        if await self.self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        
        data = json.load(open(self.database))
        with open(self.database, 'w') as db:
            data[ctx.guild.name]["prefix"] = new_prefix
            json.dump(data, db)
            
        await ctx.send("new prefix was set")
        
    @commands.command()
    async def setChannel(self, ctx, name_channel):
        """set the channel in which all messages are read by the bot"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        
        data = json.load(open(self.database))
        with open(self.database, 'w') as db:
            data[ctx.guild.name]["channel"] = name_channel
            json.dump(data, db)
            
        channel = discord.utils.get(ctx.guild.text_channels, name=name_channel)
        
        if channel is None:
            await ctx.guild.create_text_channel(name_channel)
            
        await ctx.send("channel was set")
        
        
    @commands.command()
    async def removeChannel(self, ctx):
        """remove the channel in which all messages are read by the bot"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        
        data = json.load(open(self.database))
        if "channel" in data[ctx.guild.name]:
            with open(self.database, 'w') as db:
                name_channel = data[ctx.guild.name]["channel"]
                del data[ctx.guild.name]["channel"]
                json.dump(data, db)
                
            await ctx.send("channel was delete")
            
            channel = discord.utils.get(ctx.guild.text_channels, name=name_channel)
            await channel.delete()
        else:
            await ctx.send("you don't have a channel")
        


    @commands.command()
    async def setAnnouncementsChannel(self, ctx, name_channel):
        """set the channel in which the embed command send"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        
        data = json.load(open(self.database))
        with open(self.database, 'w') as db:
            data[ctx.guild.name]["announcementsChannel"] = name_channel
            json.dump(data, db)
            
        channel = discord.utils.get(ctx.guild.text_channels, name=name_channel)
        
        if channel is None:
            await ctx.guild.create_text_channel(name_channel)
            
        await ctx.send("channel was set")
        
        
    @commands.command()
    async def removeAnnouncementsChannel(self, ctx):
        """remove the channel in which the embed command send"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        
        data = json.load(open(self.database))
        if "announcementsChannel" in data[ctx.guild.name]:
            with open(self.database, 'w') as db:
                name_channel = data[ctx.guild.name]["announcementsChannel"]
                del data[ctx.guild.name]["announcementsChannel"]
                json.dump(data, db)
                
            await ctx.send("channel was delete")
            
            channel = discord.utils.get(ctx.guild.text_channels, name=name_channel)
            await channel.delete()
        else:
            await ctx.send("you don't have a channel")
        
        
    @commands.command()
    async def setPrefixVC(self, ctx, prefixVC):
        """set the prefix for message read by the bot"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        
        data = json.load(open(self.database))
        with open(self.database, 'w') as db:
            data[ctx.guild.name]["prefixVC"] = prefixVC
            json.dump(data, db)
            
        await ctx.send("prefix vocal was set")
        

    @commands.command()
    async def removePrefixVC(self, ctx):
        """remove the prefix for message read by the bot"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        
        data = json.load(open(self.database))
        if "prefixVC" in data[ctx.guild.name]:
            with open(self.database, 'w') as db:
                del data[ctx.guild.name]["prefixVC"]
                json.dump(data, db)
                
            await ctx.send("prefix vocal was delete")
        else:
            await ctx.send("you don't have a channel")
        

    @commands.command()
    async def setLang(self, ctx, new_lang):
        """set iso language code"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        
        data = json.load(open(self.database))
        with open(self.database, 'w') as db:
            data[ctx.guild.name]["lang"] = new_lang
            json.dump(data, db)
            
        await ctx.send("new lang was set")