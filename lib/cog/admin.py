from turtle import title
import discord
from discord.ext import commands

import datetime
import json

from lib.spam_lib import Spam
from lib.robux import Robux
from lib.inventory import Inventory


class Admin(commands.Cog, name="Bot owner only"):
    def __init__(self, bot, filter_no_spam, robux, pokedex_db, inventory_db, badge_db, inventory):
        self.bot = bot
        self.filter_no_spam = filter_no_spam
        self.robux = robux
        self.inventory = inventory
        self.pokedex_db = pokedex_db
        self.inventory_db = inventory_db
        self.badge_db = badge_db

    
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
            pokedex = json.load(open(self.pokedex_db))
            description = ""
            for index in range(len(pokedex)):
                k = list(pokedex.keys())
                v = list(pokedex.values())
                if index != 0:
                    description += f"<@{k[index]}> : <:robux:1010974169552404551> {v[index]}\n"

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
    async def addBadge(self, ctx, name, emoji):
        """it adds badge from database"""

        if ctx.message.author.id == 533014724569333770:
            badge = json.load(open(self.badge_db))
            with open(self.badge_db, "w") as f_bd:
                badge[name] = emoji
                json.dump(badge, f_bd)
            await ctx.reply("badge activated")
        else:
            await ctx.reply("you don't have permissions to use this command")
            
    @commands.command()
    async def removeBadge(self, ctx, name):
        """it removes badge from database"""

        if ctx.message.author.id == 533014724569333770:
            badge = json.load(open(self.badge_db))
            
            if name in badge:
                with open(self.badge_db, "w") as f_bd:
                    del badge[name]
                    json.dump(badge, f_bd)
                await ctx.reply("badge disabled")
            else:
                await ctx.reply("badge doesn't exist")
        else:
            await ctx.reply("you don't have permissions to use this command")
            
    @commands.command()
    async def addBadgeUser(self, ctx, id, name):
        """it adds badge to user"""
        if ctx.message.author.id == 533014724569333770:
            badge = json.load(open(self.badge_db))
            inventory = json.load(open(self.inventory_db))
            
            if id in inventory and name in inventory[id]:
                await ctx.reply(f"<@{id}>, you already have the badge")
                return
            
            if name in badge:
                if not id in inventory:
                    inventory[id] = {}
                    
                with open(self.inventory_db, "w") as ind:
                    inventory[id][name] = True
                    json.dump(inventory, ind)
                await ctx.reply(f"<@{id}> gets {name} badge")
            else:
                await ctx.reply("badge doesn't exist")
        else:
            await ctx.reply("you don't have permissions to use this command")
            
    
    @commands.command()
    async def removeBadgeUser(self, ctx, id, name):
        """it removes badge to user"""
        if ctx.message.author.id == 533014724569333770:
            badge = json.load(open(self.badge_db))
            inventory = json.load(open(self.inventory_db))
            
            if name in badge:
                if id in inventory and name in inventory[id]:
                    with open(self.inventory_db, "w") as ind:
                        del inventory[id][name]
                        json.dump(inventory, ind)
                    await ctx.reply(f"<@{id}> drops {name} badge")
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
