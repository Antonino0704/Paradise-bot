import json
import discord
from discord.ext import commands

from lib.utils import Utils
from lib.spam_lib import Spam
from lib.robux import Robux
from lib.jobs import Criminal, Banker, PetSeller
from lib.cog.events import Events

class Work(commands.Cog, name="Jobs"):
    def __init__(self, bot, utils, filter_no_spam, robux, mysql_connection):
        self.bot = bot
        self.utils = utils
        self.filter_no_spam = filter_no_spam
        self.robux = robux
        self.criminal = Criminal(mysql_connection)
        self.banker = Banker(mysql_connection)
        self.petSeller = PetSeller(mysql_connection)
        self.mysql_connection = mysql_connection

    @commands.command()
    async def makeRequest(self, ctx, work_type):
        """you get a job, work type: criminal, banker, petSeller

            required:
            criminal: >10 and <50 robux
            banker: >= 50 robux
            pet seller: 1 cat"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return

        id = str(ctx.message.author.id)
        robux = self.mysql_connection.get_pokedex(id, 1)
        cat = self.mysql_connection.get_pokedex(id, 2)

        if robux:
            if work_type == "criminal" and robux >= 10 and robux < 50:
                await ctx.reply(self.criminal.add_worker(id))
                return

            elif work_type == "banker" and robux >= 50:
                await ctx.reply(self.banker.add_worker(str(ctx.message.author.id)))
                return

        if cat:
            if work_type == "petSeller":
                await ctx.reply(self.petSeller.add_worker(str(ctx.message.author.id)))
                return

        await ctx.reply("work type doesn't exist or you don't have required")

    @commands.command()
    async def resignation(self, ctx):
        """you lose your current job"""
        
        id = str(ctx.message.author.id)
        if self.criminal.check_worker(id):
            await ctx.reply(self.criminal.remove_worker(id))

        elif self.banker.check_worker(id):
            await ctx.reply(self.banker.remove_worker(id))

        elif self.petSeller.check_worker(id):
            await ctx.reply(self.petSeller.remove_worker(id))

        else:
            await ctx.reply("you don't have a job")


    @commands.command()
    async def steal(self, ctx, mention_victim):
        """you can to steal with 10% of probability the 10% of user's assets 

        if the user has houses, -5 for all old house and -10 for all modern house, the result will be your salary
        
        you can use the command every 30 seconds + the salary in seconds (ex. 3 robux are 3 seconds)
        """

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return

        mention_victim = self.utils.mention_replace(mention_victim)
        id = str(ctx.message.author.id)
        if self.criminal.check_worker(id):
            await self.criminal.working(ctx, id, mention_victim, self.robux)
        else:
            await ctx.reply("you aren't a criminal")

    @commands.command()
    async def printRobux(self, ctx):
        """you can to drop a robux, who puts reaction it gets 1 robux, while the banker gets 2 robux
        
        you can use the command every 10 minutes"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        
        id = str(ctx.message.author.id)
        if self.banker.check_worker(id):
            await self.banker.working(ctx)
        else:
            await ctx.reply("you aren't a banker")

    @commands.command()
    async def saleCat(self, ctx):
        """you can to sale a cat, who puts the reaction pays 3 robux for a cat, while pet seller gets 3 robux
        
        the salary will multiply for each cat
        if you go over 9 robux will be applicate the taxs, wallet's power is applicable

        you can use the command every 5 minutes"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        
        id = str(ctx.message.author.id)
        if self.petSeller.check_worker(id):
            await self.petSeller.working(ctx)
        else:
            await ctx.reply("you aren't a pet seller")
