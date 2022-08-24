import discord
from discord.ext import commands

from lib.spam_lib import Spam
from lib.robux import Robux


class Admin(commands.Cog, name="Owner bot only"):
    def __init__(self, bot, filter_no_spam, robux):
        self.bot = bot
        self.filter_no_spam = filter_no_spam
        self.robux = robux

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