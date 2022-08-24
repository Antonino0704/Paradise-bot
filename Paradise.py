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

from lib.cog.admin import Admin
from lib.cog.initSettings import InitSettings
from lib.cog.shop import Shop
from lib.cog.info import Info
from lib.cog.managerVC import ManagerVC

            
load_dotenv()
token = os.environ["token"]

#data files
database = 'jsonFile/database.json'
no_words_db = 'jsonFile/no_words.json'
blacklist_db = 'jsonFile/blacklist.json'
pokedex_db = 'jsonFile/pokedex.json'

intents = discord.Intents.default()
intents.members = True
intents.presences = True

utils = Utils()
filter_no_spam = Spam()
robux = Robux()

bot = commands.Bot(command_prefix=(utils.get_prefix), intents=intents)

@bot.event
async def on_ready():
    print("I'm ready")

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
        

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return        
            
    async def speak(msg):
        ctx = await bot.get_context(msg)
        
        if await utils.is_ban(ctx, filter_no_spam, robux):
            return
            
        try:
            if(os.path.exists(msg.guild.name + ".mp3")):
                os.remove(msg.guild.name+ ".mp3")
                
            if data["spam"] == "no":
                msg.content = filter_no_spam.censured(msg.author.id, msg.content)
                
            path = f"/home/raspberry/Desktop/discord_bot/songs/{msg.guild.name}.mp3"
            tts = gTTS(msg.content, lang=data["lang"])
            tts.save(f"songs/{msg.guild.name}.mp3")
                

            if not msg.guild.voice_client in bot.voice_clients:
                channel = msg.author.voice.channel
                await channel.connect()
            voice = discord.utils.get(bot.voice_clients, guild=msg.guild)
            voice.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg",
                                              source=r"/home/raspberry/Desktop/discord_bot/songs/"+ msg.guild.name +".mp3"))
            
            filter_no_spam.msg_stopped = len(msg.content)
            await robux.catch(ctx)
                   
        except AttributeError:
            await msg.channel.send("you are not connected to a voice channel", reference=msg)
        except ClientException:
            if data["spam"] == "no" and filter_no_spam.msg_stopped > 64:
                filter_no_spam.count_black_list(str(msg.author.id))
                await msg.channel.send('''Non interrompere i messaggi lunghi! 🇮🇹
Do not interrupt long messages! 🇬🇧
+1 Warn.''', reference=msg)
            #await msg.channel.send("Oh, no! something went wrong try again in a while", reference=msg)
        except ValueError:
            await msg.channel.send("language you have selected doesn't exist, please change it", reference=msg)
            
    data = json.load(open(database))[msg.guild.name]
    if msg.content[0] != data["prefix"]:

        if "prefixVC" in data:
            if msg.content[0] == data["prefixVC"]:
                await speak(msg)
                return
        if "channel" in data: 
            if msg.channel.name == data["channel"]:
                await speak(msg)
        
    await bot.process_commands(msg)
    
    
    
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
            await robux.robux(ctx, str(payload.user_id), 1)
            
    await points()
    

@bot.command()
async def Embed(ctx, description, image):
    """send embed on Announcements Channel"""

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
bot.add_cog(Admin(bot, filter_no_spam, robux))
bot.add_cog(InitSettings(bot, utils, filter_no_spam, robux, database))
bot.add_cog(Shop(bot, filter_no_spam, robux, database, pokedex_db))
bot.add_cog(Info(bot, utils, filter_no_spam, robux, pokedex_db))
bot.add_cog(ManagerVC(bot, utils, filter_no_spam, robux, database))
        
        

bot.run(token)

