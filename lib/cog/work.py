import discord
from discord.ext import commands

from lib.utils import Utils
from lib.spam_lib import Spam
from lib.robux import Robux
from lib.jobs import Criminal

class Work(commands.Cog, name="Jobs"):
    def __init__(self, bot, utils, filter_no_spam, robux):
        self.bot = bot
        self.utils = utils
        self.filter_no_spam = filter_no_spam
        self.robux = robux
        self.criminal = Criminal()

    @commands.command()
    async def makeRequest(self, ctx, work_type):
        #missing description

        if work_type == "criminal":
            await ctx.reply(self.criminal.add_worker(str(ctx.message.author.id)))
        else:
            await ctx.reply("work type doesn't exist")

    @commands.command()
    async def resignation(self, ctx):
        #missing description
        
        id = str(ctx.message.author.id)
        if self.criminal.check_worker(id):
            await ctx.reply(self.criminal.remove_worker(id))


    @commands.command()
    async def steal(self, ctx, victim_id):
        #missing description
        
        id = str(ctx.message.author.id)
        if self.criminal.check_worker(id):
            await self.criminal.working(ctx, id, victim_id, self.robux)
        else:
            await ctx.reply("you aren't a criminal")