import discord
from discord.ext import commands

import json

from lib.utils import Utils
from lib.spam_lib import Spam
from lib.robux import Robux

class Info(commands.Cog, name="Information"):
    def __init__(self, bot, utils, filter_no_spam, robux, pokedex_db, inventory_db):
        self.bot = bot
        self.utils = utils
        self.filter_no_spam = filter_no_spam
        self.robux = robux
        self.pokedex_db = pokedex_db
        self.inventory_db = inventory_db

    @commands.command()
    async def helpLang(self, ctx):
        """get link for iso code language"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        await ctx.send("all languages code: https://developers.google.com/admin-sdk/directory/v1/languages")

    @commands.command()
    async def info(self, ctx):
        """show your warns, robux and inventory"""

        pokedex = json.load(open(self.pokedex_db))
        inventory = json.load(open(self.inventory_db))
        id_s = str(ctx.message.author.id)
        
        rob = 0 if not id_s in pokedex else pokedex[id_s]
        cat = 0 if not id_s in inventory else 0 if not "cat" in inventory[id_s] else inventory[id_s]["cat"]
        old_house = 0 if not id_s in inventory else 0 if not "old_house" in inventory[id_s] else inventory[id_s]["old_house"]
        modern_house = 0 if not id_s in inventory else 0 if not "modern_house" in inventory[id_s] else inventory[id_s]["modern_house"]
        wallet = 0 if not id_s in inventory else 0 if not "wallet" in inventory[id_s] else  inventory[id_s]["wallet"]
            
        title = ctx.message.author
        description = f'''<:robux:1010974169552404551>: {rob}\n
    <a:catto:1012052395435499550>: {cat}\n
    <:oldhouse:1012052537198776430>: {old_house}\n
    <:modernhouse:1012052596120367236>: {modern_house}\n
    <a:wallet:1012053408263438396>: {bool(wallet)}\n
    warns: {self.filter_no_spam.checkWarns(str(ctx.message.author.id))}/5'''

        embed = discord.Embed(title=title, description=description)
        embed.set_image(url=ctx.message.author.avatar_url)
        await ctx.reply(embed=embed)