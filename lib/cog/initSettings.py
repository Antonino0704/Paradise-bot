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


    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def changePrefix(self, ctx, new_prefix):
        """it changes the bot prefix"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        
        data = json.load(open(self.database))
        with open(self.database, 'w') as db:
            data[ctx.guild.name]["prefix"] = new_prefix
            json.dump(data, db)
            
        await ctx.send("new prefix sets")
        

    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def setChannel(self, ctx, name_channel):
        """it sets the channel in which all messages are read by the bot"""

        channel = discord.utils.get(ctx.guild.text_channels, name=name_channel)
        
        try:
            if channel is None:
                await ctx.guild.create_text_channel(name_channel)

            if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
                return
            
            data = json.load(open(self.database))
            with open(self.database, 'w') as db:
                data[ctx.guild.name]["channel"] = name_channel
                json.dump(data, db)
                               
            await ctx.send("the channel has been set")
        except Exception as e:
            await ctx.reply(e)
        

    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def removeChannel(self, ctx):
        """it removes the channel in which all messages are read by the bot"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        
        data = json.load(open(self.database))
        if "channel" in data[ctx.guild.name]:
            try:
                name_channel = data[ctx.guild.name]["channel"]
                channel = discord.utils.get(ctx.guild.text_channels, name=name_channel)

                if channel is None:
                    await ctx.reply("the channel doesn't exist")
                    return
                await channel.delete()

                with open(self.database, 'w') as db:
                    del data[ctx.guild.name]["channel"]
                    json.dump(data, db)
                    
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
            if channel is None:
                await ctx.guild.create_text_channel(name_channel)

            if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
                return
            
            data = json.load(open(self.database))
            with open(self.database, 'w') as db:
                data[ctx.guild.name]["announcementsChannel"] = name_channel
                json.dump(data, db)
                
            await ctx.send("channel has been set")
        except Exception as e:
                await ctx.reply(e)
        
    
    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def removeAnnouncementsChannel(self, ctx):
        """it removes the channel in which the embed command sends the messages"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        
        data = json.load(open(self.database))
        if "announcementsChannel" in data[ctx.guild.name]:
            try:
                name_channel = data[ctx.guild.name]["announcementsChannel"]
                channel = discord.utils.get(ctx.guild.text_channels, name=name_channel)

                if channel is None:
                    await ctx.reply("the channel doesn't exist")
                    return
                await channel.delete()

                with open(self.database, 'w') as db:
                    del data[ctx.guild.name]["announcementsChannel"]
                    json.dump(data, db)
                    
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
        
        data = json.load(open(self.database))
        with open(self.database, 'w') as db:
            data[ctx.guild.name]["prefixVC"] = prefixVC
            json.dump(data, db)
            
        await ctx.send("prefix vocal has been set")
        

    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def removePrefixVC(self, ctx):
        """it removes the prefix for the messages the are read by the bot"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        
        data = json.load(open(self.database))
        if "prefixVC" in data[ctx.guild.name]:
            with open(self.database, 'w') as db:
                del data[ctx.guild.name]["prefixVC"]
                json.dump(data, db)
                
            await ctx.send("prefix vocal has been deleted")
        else:
            await ctx.send("you don't have a channel")
        

    @commands.command()
    async def setLang(self, ctx, new_lang):
        """it sets iso language code"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        
        data = json.load(open(self.database))
        with open(self.database, 'w') as db:
            data[ctx.guild.name]["lang"] = new_lang
            json.dump(data, db)
            
        await ctx.send("new lang was set")