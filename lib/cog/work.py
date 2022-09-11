import discord
from discord.ext import commands

from lib.utils import Utils
from lib.spam_lib import Spam
from lib.robux import Robux
from lib.jobs import Criminal, Banker

class Work(commands.Cog, name="Jobs"):
    def __init__(self, bot, utils, filter_no_spam, robux):
        self.bot = bot
        self.utils = utils
        self.filter_no_spam = filter_no_spam
        self.robux = robux
        self.criminal = Criminal()
        self.banker = Banker()


    @commands.command()
    async def myJob(self, ctx):
        #missing description

        id = str(ctx.message.author.id)

        if self.criminal.check_worker(id):
            await ctx.reply("you are a criminal")
        
        elif self.banker.check_worker(id):
            await ctx.reply("you are a banker")
        
        else:
            await ctx.reply("you don't have a job")

    @commands.command()
    async def makeRequest(self, ctx, work_type):
        #missing description and is ban

        if work_type == "criminal":
            await ctx.reply(self.criminal.add_worker(str(ctx.message.author.id)))

        elif work_type == "banker":
            await ctx.reply(self.banker.add_worker(str(ctx.message.author.id)))

        else:
            await ctx.reply("work type doesn't exist")

    @commands.command()
    async def resignation(self, ctx):
        #missing description
        
        id = str(ctx.message.author.id)
        if self.criminal.check_worker(id):
            await ctx.reply(self.criminal.remove_worker(id))

        elif self.banker.check_worker(id):
            await ctx.reply(self.banker.remove_worker(id))

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