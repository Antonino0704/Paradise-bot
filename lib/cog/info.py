import discord
from discord.ext import commands

import json

from lib.utils import Utils
from lib.spam_lib import Spam
from lib.robux import Robux

class Info(commands.Cog, name="Information"):
    def __init__(self, bot, utils, filter_no_spam, robux, mysql_connection):
        self.bot = bot
        self.utils = utils
        self.filter_no_spam = filter_no_spam
        self.robux = robux
        self.mysql_connection = mysql_connection
        self.gets_item_icon()

    def gets_item_icon(self):
        self.item_list = []
        for i in range(1, 6):
            self.item_list.append(self.mysql_connection.get_emoji_icon(i))

    @commands.command()
    async def helpLang(self, ctx):
        """you get link for iso code language"""

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return
        await ctx.send("all languages code: https://developers.google.com/admin-sdk/directory/v1/languages")

    @commands.command()
    async def infoItem(self, ctx, item_name):
        """shows item information"""

        data = self.mysql_connection.get_info("name", item_name, "items")
        if data:
            embed = discord.Embed(title=data[0][0], description=data[0][1])
            return await ctx.reply(embed=embed)
        await ctx.reply("item doesn't exist")

    @commands.command()
    async def infoJob(self, ctx, work_type):
        """shows job information
    work type: criminal, banker, petSeller"""

        data = self.mysql_connection.get_info("name", work_type, "jobs")
        if data:
            embed = discord.Embed(title=data[0][0], description=data[0][1])
            return await ctx.reply(embed=embed)
        await ctx.reply("job doesn't exist")

    @commands.command()
    async def infoBadge(self, ctx, badge_name):
        """shows badge informationr"""

        data = self.mysql_connection.get_info("name", badge_name, "badges")
        if data:
            embed = discord.Embed(title=data[0][0], description=data[0][1])
            embed.set_footer(text=f"you got that: {self.mysql_connection.get_badge_date(ctx.message.author.id, badge_name)}")
            return await ctx.reply(embed=embed)
        await ctx.reply("badge doesn't exist")

    @commands.command()
    async def info(self, ctx):
        """it shows your warns, robux, inventory and job"""
        
        id_s = str(ctx.message.author.id)
        items = self.mysql_connection.get_pokedex_all(id_s)
        badges = self.getBadge(id_s)
        job = self.mysql_connection.get_user_job(id_s)
        title = str(ctx.message.author) + badges

        names = self.mysql_connection.get_user_names(id_s, "firstname, lastname")
        names = names[0][0] + " " + names[0][1] if names else "no firstname no lastname"

        description = ""
        for icon, amount in items:
            description += f'''
    {icon}: {amount}\n
            '''
        description += f'''
    Job: {job}    
        '''

        embed = discord.Embed(title=title, description=description)
        embed.set_image(url=ctx.message.author.avatar_url)
        embed.set_footer(text=names)
        await ctx.reply(embed=embed)
    
    def getBadge(self, id):
        badge_str = " "
        badges = self.mysql_connection.get_badge_icon_all(id)
        for i in badges:
            badge_str += i[0] + " "
        return badge_str
            