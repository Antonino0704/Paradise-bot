import json
import discord
from lib.spam_lib import Spam
from lib.robux import Robux


class Utils:
    def __init__(self):
        self.data_files()
        
    def data_files(self):
        self.database = 'jsonFile/database.json'
        
    def get_prefix(self, bot, msg):
        data = json.load(open(self.database))
        return data[msg.guild.name]["prefix"]
    
    async def is_ban(self, ctx, filter_no_spam, robux):
        if filter_no_spam.check_black_list(str(ctx.message.author.id)):
            if robux.less_one_robux(str(ctx.message.author.id)):
                await ctx.reply("-1 <:robux:1010974169552404551>")
                
            await ctx.reply("you are banned")
            return True
        return False
    
    async def disconnection_for_inactivity(self, guild, n):
        try:
            channel = guild.text_channels[n]
            await channel.send("disconection for inactivity")
        except:
            return await self.disconnection_for_inactivity(guild, n+1)