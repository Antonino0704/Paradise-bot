from discord import *
from discord.ext import commands
import discord.utils

from gtts import gTTS
from dotenv import load_dotenv
import json
import os
import datetime

from lib.utils import Utils
from lib.spam_lib import Spam
from lib.robux import Robux
from lib.inventory import Inventory
from lib.jobs import *

from lib.cog.admin import Admin
from lib.cog.initSettings import InitSettings
from lib.cog.shop import Shop
from lib.cog.info import Info
from lib.cog.managerVC import ManagerVC
from lib.cog.work import Work
from lib.cog.events import Events

            
load_dotenv()
token = os.environ["token"]

#data files
database = 'jsonFile/database.json'
no_words_db = 'jsonFile/no_words.json'
blacklist_db = 'jsonFile/blacklist.json'
pokedex_db = 'jsonFile/pokedex.json'
inventory_db = 'jsonFile/inventory.json'
jobs_db = 'jsonFile/jobs.json'
badge_db = 'jsonFile/badge.json'

intents = discord.Intents.default()
intents.members = True
intents.presences = True

utils = Utils()
filter_no_spam = Spam()
robux = Robux()
inventory = Inventory()

queue = {}

bot = commands.Bot(command_prefix=(utils.get_prefix), intents=intents)

@bot.event
async def on_ready():
    print("I'm ready")
    for guild in bot.guilds:
        queue[guild.name] = {}
        queue[guild.name]["content"] = []
        queue[guild.name]["status"] = False

@bot.event
async def on_guild_join(guild):
    data = json.load(open(database))
    data[guild.name] = {}
    with open(database, 'w') as db:
        data[guild.name]["prefix"] = "$"
        data[guild.name]["lang"] = "en"
        data[guild.name]["spam"] = "yes"
        json.dump(data, db)
        

@bot.event
async def on_guild_update(before, after):
    if before.name != after.name:
        data = json.load(open(database))
        with open(database, 'w') as db:
            data[after.name]= data[before.name]
            del data[before.name]
            json.dump(data, db)
        
        del queue[before.name]
        queue[after.name] = {}
        queue[after.name]["content"] = []
        queue[after.name]["status"] = False

@bot.event
async def on_raw_reaction_add(payload):
    if bot.get_user(payload.user_id) == bot.user or str(payload.emoji) != "<:robux:1010974169552404551>":
        return
 
    async def points():
        channel = bot.get_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        ctx = await bot.get_context(msg)
        if msg.content == "<:robux:1010974169552404551> oh a wild robux appeared, you put the reaction to win it!!" and msg.author == bot.user:
            if await utils.is_ban(ctx, filter_no_spam, robux):
                return
            
            await msg.clear_reactions()
            await msg.edit(content=f"<@{payload.user_id}> you win")
            try:
                await robux.robux(ctx, str(payload.user_id), 1)
            except Exception:
                await asyncio.sleep(10)
                await robux.robux(ctx, str(payload.user_id), 1)
       
    try:
        await points()
    except Exception:
        await bot.get_channel(payload.channel_id).send(f"<@{payload.user_id}> sorry somethings went wrong")
    

@bot.command()
async def Embed(ctx, description, image):
    """you send embed on Announcements Channel"""

    if await utils.is_ban(ctx, filter_no_spam, robux):
        return
        
    data = json.load(open(database))[ctx.guild.name]

    if not "announcementsChannel" in data:
        await ctx.send(f"set a announcements channel, {data['prefix']}setAnnouncementsChannel")
        return
    
    channel = discord.utils.get(ctx.guild.text_channels, name=data["announcementsChannel"])
    
    embed = discord.Embed(description=description, timestamp=datetime.datetime.utcnow())
    embed.set_image(url=image)
    
    await channel.send(embed=embed)
    

#cog
bot.add_cog(Admin(bot, filter_no_spam, robux, pokedex_db, 
                inventory_db, badge_db, inventory))

bot.add_cog(InitSettings(bot, utils, filter_no_spam, robux, 
            database))

bot.add_cog(Shop(bot, utils, filter_no_spam, robux, 
                inventory, database, pokedex_db, inventory_db, 
                jobs_db))

bot.add_cog(Info(bot, utils, filter_no_spam, robux, 
                pokedex_db, inventory_db, jobs_db, badge_db))

bot.add_cog(ManagerVC(bot, utils, filter_no_spam, robux, 
                    database, queue))
                    
bot.add_cog(Work(bot, utils, filter_no_spam, robux,
            pokedex_db, inventory_db))

bot.add_cog(Events(bot, utils, filter_no_spam, robux,
                   inventory_db))

bot.run(token)