import json
import discord
from discord.ext import commands

from lib.utils import Utils
from lib.spam_lib import Spam
from lib.robux import Robux
from lib.jobs import Criminal, Banker, PetSeller

class Work(commands.Cog, name="Jobs"):
    def __init__(self, bot, utils, filter_no_spam, robux, pokedex_db, inventory_db):
        self.bot = bot
        self.utils = utils
        self.filter_no_spam = filter_no_spam
        self.robux = robux
        self.pokedex_db = pokedex_db
        self.inventory_db = inventory_db
        self.criminal = Criminal()
        self.banker = Banker()
        self.petSeller = PetSeller()

    @commands.command()
    async def makeRequest(self, ctx, work_type):
        #missing description and is ban

        pokedex = json.load(open(self.pokedex_db))
        inventory = json.load(open(self.inventory_db))
        id = str(ctx.message.author.id)

        if id in pokedex:
            if work_type == "criminal" and pokedex[id] >= 10 and pokedex[id] < 50:
                await ctx.reply(self.criminal.add_worker(id))
                return

            elif work_type == "banker" and pokedex[id] >= 50:
                await ctx.reply(self.banker.add_worker(str(ctx.message.author.id)))
                return

        if id in inventory:
            if work_type == "petSeller" and "cat" in inventory[id]:
                await ctx.reply(self.petSeller.add_worker(str(ctx.message.author.id)))
                return

        await ctx.reply("work type doesn't exist or you don't have required")

    @commands.command()
    async def resignation(self, ctx):
        #missing description
        
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
        #missing description and is ban

        mention_victim = self.utils.mention_replace(mention_victim)
        id = str(ctx.message.author.id)
        if self.criminal.check_worker(id):
            await self.criminal.working(ctx, id, mention_victim, self.robux)
        else:
            await ctx.reply("you aren't a criminal")

    @commands.command()
    async def printRobux(self, ctx):
        #missing description and is ban
        
        id = str(ctx.message.author.id)
        if self.banker.check_worker(id):
            await self.banker.working(ctx)
        else:
            await ctx.reply("you aren't a banker")

    @commands.command()
    async def saleCat(self, ctx):
        #missing description and is ban
        
        id = str(ctx.message.author.id)
        if self.petSeller.check_worker(id):
            await self.petSeller.working(ctx)
        else:
            await ctx.reply("you aren't a pet seller")