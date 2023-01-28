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

    
    @commands.command()
    async def embedAdmin(self, ctx, title, description, url_image):
        """it sends embed to all bot's guilds"""

        if ctx.message.author.id == 533014724569333770:
            embed = discord.Embed(title=title, description=description, timestamp=datetime.datetime.utcnow())
            embed.set_image(url=url_image)
            embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
            for guild in self.bot.guilds:
                await self.embed_admin_channel(embed, guild, 0)
        else:
            await ctx.reply("you don't have permissions to use this command")

    
    async def embed_admin_channel(self, embed, guild, n):
        try:
            channel = guild.text_channels[n]
            await channel.send(embed=embed)
        except:
            return await self.embed_admin_channel(embed, guild, n+1)

    @commands.command()
    async def blackList(self, ctx, id):
        """it adds user to blacklist"""

        if ctx.message.author.id == 533014724569333770:
            await self.filter_no_spam.add_black_list(ctx, id)
        else:
            await ctx.reply("you don't have permissions to use this command")
            

    @commands.command()
    async def removeBlackList(self, ctx, id):
        """it removes user from blacklist"""

        if ctx.message.author.id == 533014724569333770:
            await self.filter_no_spam.remove_black_list(ctx, id)
        else:
            await ctx.reply("you don't have permissions to use this command")
            

    @commands.command()
    async def addNoWords(self, ctx, *, words):
        """it adds word or words in prohibited words list"""

        if ctx.message.author.id == 533014724569333770:
            words = words.replace("\n", " ")
            words = words.split(" ")
            await self.filter_no_spam.add_no_words(ctx,words)
        else:
            await ctx.reply("you don't have permissions to use this command")
            
            
    @commands.command()
    async def removeNoWords(self, ctx, *, words):
        """it removes word or words from prohibited words list"""

        if ctx.message.author.id == 533014724569333770:
            words = words.replace("\n", " ")
            words = words.split(" ")
            await self.filter_no_spam.remove_no_words(ctx, words)
        else:
            await ctx.reply("you don't have permissions to use this command")
            
            
    @commands.command()
    async def money(self, ctx, id, robux_number):
        """it adds or remove robux from user"""

        if ctx.message.author.id == 533014724569333770:
            robux_number = int(robux_number)
            await self.robux.robux(ctx, id, robux_number)
        else:
            await ctx.reply("you don't have permissions to use this command")

    @commands.command()
    async def inventory(self, ctx, id, type_object, number):
        """it adds or remove every type of item from inventory"""

        if ctx.message.author.id == 533014724569333770:
            number = int(number)
            await self.inventory.buy_object(ctx, id, type_object, number)
        else:
            await ctx.reply("you don't have permissions to use this command")


    @commands.command()
    async def getRobuxList(self, ctx):
        """it sends the list of users who have the robux"""

        if ctx.message.author.id == 533014724569333770:
            robux_list = self.mysql_connection.get_robux_list()
            description = ""
            for index in robux_list:
                description += f"<@{index[0]}> : <:robux:1010974169552404551> {index[1]}\n"

                if len(description) > 3000 and len(description) < 4096:
                    embed = discord.Embed(title="Robux user list", description=description)
                    await ctx.send(embed=embed)
                    description = ""

            if description != None:
                embed = discord.Embed(title="Robux user list", description=description)
                await ctx.send(embed=embed)
        else:
            await ctx.reply("you don't have permissions to use this command")
            
    @commands.command()
    async def addBadge(self, ctx, name, emoji, description = "no description"):
        """it adds badge to database"""

        if ctx.message.author.id == 533014724569333770:
            self.mysql_connection.add_badge(name, description, emoji)
            await ctx.reply("badge activated")
        else:
            await ctx.reply("you don't have permissions to use this command")
            
    @commands.command()
    async def removeBadge(self, ctx, emoji):
        """it removes badge from database"""

        if ctx.message.author.id == 533014724569333770:
            badge_id = self.mysql_connection.get_badge_by_icon(emoji)
            if not self.mysql_connection.is_exist("badge_id", badge_id, "badges", "badge_id"):
                self.mysql_connection.remove_badges(badge_id)
                await ctx.reply("badge disabled")
            else:
                await ctx.reply("badge doesn't exist")
        else:
            await ctx.reply("you don't have permissions to use this command")
            
    @commands.command()
    async def addBadgeUser(self, ctx, id, emoji):
        """it adds badge to user"""
        if ctx.message.author.id == 533014724569333770:
            badge_id = self.mysql_connection.get_badge_by_icon(emoji)

            if not self.mysql_connection.is_exist_composite("user_id", "badge_id", id, badge_id, "inventories", "received"):
                await ctx.reply(f"<@{id}>, you already have the badge")
                return
            
            if not self.mysql_connection.is_exist("badge_id", badge_id, "badges", "badge_id"):
                if self.mysql_connection.is_exist("user_id", id, "users", "user_id"):
                    self.mysql_connection.add_user(id)
                    
                self.mysql_connection.add_badge_to_user(id, badge_id)
                await ctx.reply(f"<@{id}> gets {emoji} badge")
            else:
                await ctx.reply("badge doesn't exist")
        else:
            await ctx.reply("you don't have permissions to use this command")
            
    
    @commands.command()
    async def removeBadgeUser(self, ctx, id, emoji):
        """it removes badge to user"""
        if ctx.message.author.id == 533014724569333770:
            badge_id = self.mysql_connection.get_badge_by_icon(emoji)

            if not self.mysql_connection.is_exist("badge_id", badge_id, "badges", "badge_id"):

                if not self.mysql_connection.is_exist_composite("user_id", "badge_id", id, badge_id, "inventories", "received"):
                    self.mysql_connection.delete_badge_to_user(id, badge_id)
                    await ctx.reply(f"<@{id}> drops {emoji} badge")
                else:      
                    await ctx.reply(f"<@{id}>, you don't have the badge")
            else:
                await ctx.reply("badge doesn't exist")
        else:
            await ctx.reply("you don't have permissions to use this command")


    @commands.command()
    async def getEmoji(self, ctx, msg):
        """you get emoji like to string"""

        if ctx.message.author.id == 533014724569333770:
            msg = msg.replace("<", "")
            await ctx.reply(msg)
        else:
            await ctx.reply("you don't have permissions to use this command")

    @commands.command() 
    async def responding(self, ctx, id_message, id_channel, text): 
        """you send a message like to bot""" 

        if ctx.message.author.id == 533014724569333770:
            try: 
                channel = self.bot.get_channel(int(id_channel))
                msg = await channel.fetch_message(id_message)
                ctx_msg = await self.bot.get_context(msg) 
                await ctx_msg.reply(text)
            except:
                await ctx.reply("error message or channel not found") 
        else:
            await ctx.reply("you don't have permissions to use this command") 
