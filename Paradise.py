from discord import *
from discord.ext import commands
import discord.utils

from gtts import gTTS
from dotenv import load_dotenv
import json
import os
import datetime
import asyncio

from lib.utils import Utils
from lib.spam_lib import Spam
from lib.robux import Robux
from lib.inventory import Inventory
from lib.jobs import *
from lib.mysql import Mysql

from lib.cog.admin import Admin
from lib.cog.initSettings import InitSettings
from lib.cog.shop import Shop
from lib.cog.info import Info
from lib.cog.managerVC import ManagerVC
from lib.cog.work import Work
from lib.cog.events import Events

            
load_dotenv()
token = os.environ["token"]

intents = discord.Intents.all()
intents.members = True
intents.presences = True

mysql_connection = Mysql(os.environ["address"], os.environ["usr"], os.environ["passwd"])
utils = Utils(mysql_connection)
filter_no_spam = Spam(mysql_connection)
robux = Robux(mysql_connection)
inventory = Inventory(mysql_connection)

queue = {}

bot = commands.Bot(command_prefix=(utils.get_prefix), intents=intents)



def queue_init(name):
    queue[name] = {}
    queue[name]["content"] = []
    queue[name]["status"] = False

@bot.event
async def on_ready():
    print("I'm ready")
    await bot.tree.sync()
    for guild in bot.guilds:
        queue_init(guild.name)

@bot.event
async def on_guild_join(guild):
    mysql_connection.guild_join(guild.id, guild.name)
    queue_init(guild.name)
 
@bot.event
async def on_guild_update(before, after):
    if before.name != after.name:
        del queue[before.name]
        queue_init(after.name)

@bot.event
async def on_raw_reaction_add(payload):
    emj = mysql_connection.get_emoji_icon(1)
    if bot.get_user(payload.user_id) == bot.user or str(payload.emoji) != emj:
        return
 
    async def points():
        channel = bot.get_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        ctx = await bot.get_context(msg)
        if msg.content == f"{emj} oh! a wild robux appeared, use the reaction to win it!!" and msg.author == bot.user:
            if await utils.is_ban(ctx, filter_no_spam, robux):
                return
            
            await msg.clear_reactions()
            await msg.edit(content=f"<@{payload.user_id}> you win!")
            try:
                await robux.robux(ctx, str(payload.user_id), 1)
            except Exception:
                await asyncio.sleep(10)
                await robux.robux(ctx, str(payload.user_id), 1)
       
    try:
        await points()
    except Exception:
        await bot.get_channel(payload.channel_id).send(f"<@{payload.user_id}> sorry, something went wrong")
    

@bot.command()
async def Embed(ctx, description, image):
    """you send an embed on Announcements Channel"""

    if await utils.is_ban(ctx, filter_no_spam, robux):
        return
        
    if mysql_connection.is_exist("guild_id", ctx.guild.id, "guilds", "announcementsChannel"):
        prefix = mysql_connection.get_guild_data(ctx.guild.id, "prefix")
        await ctx.send(f"set an announcements channel, {prefix}setAnnouncementsChannel")
        return

    channel = discord.utils.get(ctx.guild.text_channels, name=mysql_connection.get_guild_data(ctx.guild.id, "announcementsChannel"))
    
    embed = discord.Embed(description=description, timestamp=datetime.datetime.utcnow())
    embed.set_image(url=image)
    
    await channel.send(embed=embed)    


#bot.run(token)

async def load_cogs():
    #cog
    await bot.add_cog(Admin(bot, filter_no_spam, robux, inventory, 
                    mysql_connection))

    await bot.add_cog(InitSettings(bot, utils, filter_no_spam, robux, 
                    mysql_connection))

    await bot.add_cog(Shop(bot, utils, filter_no_spam, robux, 
                    inventory, mysql_connection))

    await bot.add_cog(Info(bot, utils, filter_no_spam, robux, 
                    mysql_connection))

    await bot.add_cog(ManagerVC(bot, os.environ["songs"], os.environ["ffmpeg"], utils, filter_no_spam, robux, 
                    queue, mysql_connection))
                        
    await bot.add_cog(Work(bot, utils, filter_no_spam, robux,
                    mysql_connection))

    await bot.add_cog(Events(bot, utils, filter_no_spam, robux,
                    mysql_connection))

async def main():
    await load_cogs()
    await bot.start(token)
    

asyncio.run(main())
