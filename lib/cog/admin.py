from turtle import title
import discord
from discord.ext import commands

import datetime
import json

from lib.spam_lib import Spam
from lib.robux import Robux
from lib.inventory import Inventory


class Admin(commands.Cog, name="Owner bot only"):
    def __init__(self, bot, filter_no_spam, robux, pokedex_db, inventory):
        self.bot = bot
        self.filter_no_spam = filter_no_spam
        self.robux = robux
        self.inventory = inventory
        self.pokedex_db = pokedex_db

    
    @commands.command()
    async def embedAdmin(self, ctx, title, description, url_image):
        """send embed in all guilds of the bot"""

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
        """add user to blacklist"""

        if ctx.message.author.id == 533014724569333770:
            await self.filter_no_spam.add_black_list(ctx, id)
        else:
            await ctx.reply("you don't have permissions to use this command")
            

    @commands.command()
    async def removeBlackList(self, ctx, id):
        """remove user to blacklist"""

        if ctx.message.author.id == 533014724569333770:
            await self.filter_no_spam.remove_black_list(ctx, id)
        else:
            await ctx.reply("you don't have permissions to use this command")
            

    @commands.command()
    async def addNoWords(self, ctx, *, words):
        """add word or words in prohibited words list"""

        if ctx.message.author.id == 533014724569333770:
            words = words.replace("\n", " ")
            words = words.split(" ")
            await self.filter_no_spam.add_no_words(ctx,words)
        else:
            await ctx.reply("you don't have permissions to use this command")
            
            
    @commands.command()
    async def removeNoWords(self, ctx, *, words):
        """remove word or words in prohibited words list"""

        if ctx.message.author.id == 533014724569333770:
            words = words.replace("\n", " ")
            words = words.split(" ")
            await self.filter_no_spam.remove_no_words(ctx, words)
        else:
            await ctx.reply("you don't have permissions to use this command")
            
            
    @commands.command()
    async def money(self, ctx, id, robux_number):
        """add or remove robux to user"""

        if ctx.message.author.id == 533014724569333770:
            robux_number = int(robux_number)
            await self.robux.robux(ctx, id, robux_number)
        else:
            await ctx.reply("you don't have permissions to use this command")

    @commands.command()
    async def inventory(self, ctx, id, type_object, number):
        """add or remove every type of object on inventory"""

        if ctx.message.author.id == 533014724569333770:
            number = int(number)
            await self.inventory.buy_object(ctx, id, type_object, number)
        else:
            await ctx.reply("you don't have permissions to use this command")


    @commands.command()
    async def getListRobux(self, ctx):
        #missing description

        if ctx.message.author.id == 533014724569333770:
            pokedex = json.load(open(self.pokedex_db))
            description = ""
            for index in range(len(pokedex)):
                k = list(pokedex.keys())
                v = list(pokedex.values())
                if index != 0:
                    description += f"<@{k[index]}> : <:robux:1010974169552404551> {v[index]}\n"

                if len(description) > 3000 and len(description) < 4096:
                    embed = discord.Embed(title="List robux", description=description)
                    await ctx.send(embed=embed)
                    description = ""

            if description != None:
                embed = discord.Embed(title="List robux", description=description)
                await ctx.send(embed=embed)
        else:
            await ctx.reply("you don't have permissions to use this command")
        