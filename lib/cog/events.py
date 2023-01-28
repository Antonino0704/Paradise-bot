import discord
from discord.ext import commands

import json
import random
import asyncio

from lib.utils import Utils
from lib.spam_lib import Spam
from lib.robux import Robux

class Events(commands.Cog, name="events"):
    def __init__(self, bot, utils, filter_no_spam, robux, mysql_connection):
        self.bot = bot
        self.utils = utils
        self.filter_no_spam = filter_no_spam
        self.robux = robux
        self.mysql_connection = mysql_connection
        self.gets_emoji()

    def gets_emoji(self):
        self.halloween_emoji = self.mysql_connection.get_badge_icon(3)
        self.christmas = self.mysql_connection.get_badge_icon(4)
        self.new_year2023 = self.mysql_connection.get_badge_icon(5)
    
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
        if self.bot.get_user(payload.user_id) == self.bot.user or self.mysql_connection.is_exist("icon", str(payload.emoji), "badges", "name") : 
            return
    
        async def points():
            channel = self.bot.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            ctx = await self.bot.get_context(msg)

            #halloween
            if msg.content == f"{self.halloween_emoji}Happy Halloween{self.halloween_emoji}" and msg.author == self.bot.user:
                await self.event_award(ctx, str(payload.user_id), str(payload.emoji), msg, "halloween", "halloweenAward")

            #christmas
            if msg.content == f"{self.christmas}Happy christmas{self.christmas}" and msg.author == self.bot.user:
                await self.event_award(ctx, str(payload.user_id), str(payload.emoji), msg, "christmas", "christmas")

            #2023year
            if msg.content == f"{self.new_year2023}Happy new year{self.new_year2023}" and msg.author == self.bot.user:
                await self.event_award(ctx, str(payload.user_id), str(payload.emoji), msg, "new year", "2023")
          
        await points()
            
    async def event_award(self, ctx, id, badge_icon, msg, name_event, badge_name):
        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return

        badge_id = self.mysql_connection.get_badge_by_icon(badge_icon)
        if not self.mysql_connection.is_exist_composite("user_id", "badge_id", id, badge_id, "inventories", "received"):
            await ctx.reply(f"<@{id}>, you already have the {name_event} badge")
            return
        
        if self.mysql_connection.is_exist("user_id", id, "users", "user_id"):
            self.mysql_connection.add_user(id)
        
        self.mysql_connection.add_badge_to_user(id, badge_id)
        await ctx.reply(f"<@{id}> gets {name_event} badge")
        await msg.clear_reactions()     
