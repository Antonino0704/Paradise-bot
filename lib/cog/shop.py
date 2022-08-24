import discord
from discord.ext import commands

import json

from lib.spam_lib import Spam
from lib.robux import Robux

class Shop(commands.Cog, name="Shop"):
    def __init__(self, bot, filter_no_spam, robux, database, pokedex_db):
        self.bot = bot
        self.filter_no_spam = filter_no_spam
        self.robux = robux
        self.database = database
        self.pokedex_db = pokedex_db

    @commands.command()
    async def shop(self, ctx):
        """shown the shop"""

        prefix = json.load(open(self.database))[ctx.guild.name]["prefix"]
        await ctx.reply(f'''{ctx.message.author.name} welcome at shop

    Remove ban: <:robux:1010974169552404551> 40 <:4596froggyarrow:1011296133131292692> {prefix}help Rban
    Change bot activity: <:robux:1010974169552404551> 10 <:4596froggyarrow:1011296133131292692> {prefix}help ChangeActivity
    ''')
        
    @commands.command()
    async def Rban(self, ctx):
        """payment 40 robux for the remove of the blacklist"""

        pokedex = json.load(open(self.pokedex_db))
        id = str(ctx.message.author.id)
        price = 40
        
        if id in pokedex and pokedex[id] >= price:
            await self.filter_no_spam.remove_black_list(ctx, id)
            await self.robux.payment(ctx, id, pokedex, price)
        else:
            await ctx.reply(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")
            

    @commands.command()
    async def ChangeActivity(self, ctx, game):
        """payment 10 robux for change activity of the bot"""

        pokedex = json.load(open(self.pokedex_db))
        id = str(ctx.message.author.id)
        price = 10
        game = self.filter_no_spam.censured(ctx.message.author.id, game)
        if id in pokedex and pokedex[id] >= price:
            await self.bot.change_presence(activity=discord.Game(name=game))
            await self.robux.payment(ctx, id, pokedex, price)
        else:
            await ctx.reply(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")