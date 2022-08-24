import discord
from discord.ext import commands

import json

from lib.utils import Utils
from lib.spam_lib import Spam
from lib.robux import Robux

class Info(commands.Cog, name="Information"):
    def __init__(self, bot, utils, filter_no_spam, robux, pokedex_db):
        self.bot = bot
        self.utils = utils
        self.filter_no_spam = filter_no_spam
        self.robux = robux
        self.pokedex_db = pokedex_db

    @commands.command()
    async def helpLang(self, ctx):
        """get link for iso code language"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        await ctx.send("all languages code: https://developers.google.com/admin-sdk/directory/v1/languages")

    @commands.command()
    async def info(self, ctx):
        """show your warns and robux"""

        pokedex = json.load(open(self.pokedex_db))
        id_s = str(ctx.message.author.id)
        if id_s in pokedex:
            await ctx.reply(f'''{ctx.message.author.name}

    <:robux:1010974169552404551>: {pokedex[id_s]}
    warns: {self.filter_no_spam.checkWarns(str(ctx.message.author.id))}/5''')
            return
            
        await ctx.reply(f'''{ctx.message.author.name}

    <:robux:1010974169552404551>: 0
    warns: {self.filter_no_spam.checkWarns(str(ctx.message.author.id))}/5''')