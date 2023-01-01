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

    
    @staticmethod
    def generate_probably(start, end, limit):
        number = random.randint(1, limit)
        if number >= start and number <= end:
            return True
        return False
    
    @staticmethod
    async def event_message(ctx, emoji, event_name, start, end, limit):
        if Events.generate_probably(start, end, limit):
            msg = await ctx.send(f"{emoji}Happy {event_name}{emoji}")
            await msg.add_reaction(f"{emoji}")
        
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.bot.get_user(payload.user_id) == self.bot.user or str(payload.emoji) != "<a:halloween:1032777226397175920>":
            return
    
        async def points():
            channel = self.bot.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            ctx = await self.bot.get_context(msg)

            #halloween
            if msg.content == "<a:halloween:1032777226397175920>Happy Halloween<a:halloween:1032777226397175920>" and msg.author == self.bot.user:
                try:
                    await self.event_award(ctx, str(payload.user_id), msg, "halloween", "halloweenAward")
                except Exception:
                    await asyncio.sleep(10)
                    await self.event_award(ctx, str(payload.user_id), msg, "halloween", "halloweenAward")
          
        await points()
            
    async def event_award(self, ctx, id, msg, name_event, badge_name):
        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        
        inventory = json.load(open(self.inventory_db))
        
        if id in inventory and badge_name in inventory[id]:
            await ctx.reply(f"<@{id}>, you already have the {name_event} badge")
            return
        
        if not id in inventory:
            inventory[id] = {}
        
        with open(self.inventory_db, "w") as ind:
            inventory[id][badge_name] = True
            json.dump(inventory, ind)
            await ctx.reply(f"<@{id}> gets {name_event} badge")
            await msg.clear_reactions()     