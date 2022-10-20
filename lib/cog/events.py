import discord
from discord.ext import commands

import json
import random

from lib.utils import Utils
from lib.spam_lib import Spam
from lib.robux import Robux

class Events(commands.Cog, name="events"):
    def __init__(self, bot, utils, filter_no_spam, robux, inventory_db):
        self.bot = bot
        self.utils = utils
        self.filter_no_spam = filter_no_spam
        self.robux = robux
        self.inventory_db = inventory_db
        
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.bot.get_user(payload.user_id) == self.bot.user or str(payload.emoji) != "<a:halloween:1032777226397175920>":
            return
    
        async def points():
            channel = self.bot.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            ctx = await self.bot.get_context(msg)
            if msg.content == "<a:halloween:1032777226397175920>Happy Halloween<a:halloween:1032777226397175920>" and msg.author == self.bot.user:
                await self.halloween_award(ctx, str(payload.user_id), msg)
          
        await points()
        
    def generate_probably(self, start, end, limit):
        number = random.randint(1, limit)
        if number >= start and number <= end:
            return True
        return False
    
    async def halloween_message(self, ctx):
        if self.generate_probably(1, 1, 100):
            msg = await ctx.send("<a:halloween:1032777226397175920>Happy Halloween<a:halloween:1032777226397175920>")
            await msg.add_reaction("<a:halloween:1032777226397175920>")
            
    async def halloween_award(self, ctx, id, msg):
        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        
        inventory = json.load(open(self.inventory_db))
        
        if id in inventory and "halloweenAward" in inventory[id]:
            await ctx.reply(f"<@{id}>, you already have the halloween badge")
            return
        
        if not id in inventory:
            inventory[id] = {}
        
        with open(self.inventory_db, "w") as ind:
            inventory[id]["halloweenAward"] = True
            json.dump(inventory, ind)
            await ctx.reply(f"<@{id}> gets halloween badge")
            await msg.clear_reactions()
        
        