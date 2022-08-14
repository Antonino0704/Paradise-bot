from discord import *
from discord.ext import commands
from gtts import gTTS
from dotenv import load_dotenv
import discord.utils
import json
import os
import datetime


class Utils:
    def __init__(self):
        pass
    
    def get_prefix(self, bot, msg):
        data = json.load(open(database))
        return data[msg.guild.name]["prefix"]
    
class Spam:
    def __init__(self):
        self.no_spam = {}
        self.msg_stopped = 0
        self.no_words = json.load(open("no_words.json"))["no_words"]
        
    def check_black_list(self, id):
        black_list = json.load(open("blacklist.json"))
        if id in black_list:
            diff = datetime.datetime.now() - datetime.datetime.strptime(black_list[id], "%d-%b-%Y (%H:%M:%S.%f)")
            
            if diff.total_seconds() / 60 > 180:
                with open("blacklist.json", 'w') as bl:
                    del black_list[id]
                    json.dump(black_list, bl)
                return False
            return True
        
        return False
    
    def count_black_list(self, id):
        if not id in self.no_spam:
            self.no_spam[id] = [0, datetime.datetime.now()]
            
        diff = datetime.datetime.now() - self.no_spam[id][1]
        if diff.total_seconds() / 60 > 10:
            self.no_spam[id] = [1, datetime.datetime.now()]
        else:
            self.no_spam[id][0] += 1
            self.no_spam[id][1] = datetime.datetime.now()
            
        if self.no_spam[id][0] >= 5:
            black_list = json.load(open("blacklist.json"))
            with open("blacklist.json", 'w') as bl:
                black_list[id] = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
                json.dump(black_list, bl)
                del self.no_spam[id]
                
    def checkWarns(self, id):
        if id in self.no_spam:
            diff = datetime.datetime.now() - self.no_spam[id][1]
            if diff.total_seconds() / 60 > 10:
                return 0
            return self.no_spam[id][0]
        
        return 0
    
    def censured(self, id, msg):
        if id != 533014724569333770:
            for word in self.no_words:
                msg = msg.replace(word, "*")
        return msg
            
load_dotenv()
token = os.environ["token"]
database = 'database.json'

intents = discord.Intents.default()
intents.members = True
intents.presences = True

utils = Utils()
filter_no_spam = Spam()

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
        if filter_no_spam.check_black_list(str(msg.author.id)):
            await msg.channel.send("you are banned", reference=msg)
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
    
    

@bot.command()
async def Embed(ctx, description, image):
    data = json.load(open(database))[ctx.guild.name]

    if not "announcementsChannel" in data:
        await ctx.send(f"set a announcements channel, {data['prefix']}setAnnouncementsChannel")
        return
    
    channel = discord.utils.get(ctx.guild.text_channels, name=data["announcementsChannel"])
    
    embed = discord.Embed(description=description, timestamp=datetime.datetime.utcnow())
    embed.set_image(url=image)
    
    await channel.send(embed=embed)

    
@bot.command()
async def changePrefix(ctx, new_prefix):
    if filter_no_spam.check_black_list(str(ctx.message.author.id)):
        await ctx.reply("you are banned")
        return
    
    data = json.load(open(database))
    with open(database, 'w') as db:
        data[ctx.guild.name]["prefix"] = new_prefix
        json.dump(data, db)
        
    await ctx.send("new prefix was set")
    
@bot.command()
async def setChannel(ctx, name_channel):
    if filter_no_spam.check_black_list(str(ctx.message.author.id)):
        await ctx.reply("you are banned")
        return
    
    data = json.load(open(database))
    with open(database, 'w') as db:
        data[ctx.guild.name]["channel"] = name_channel
        json.dump(data, db)
        
    channel = discord.utils.get(ctx.guild.text_channels, name=name_channel)
    
    if channel is None:
        await ctx.guild.create_text_channel(name_channel)
        
    await ctx.send("channel was set")
    
    
@bot.command()
async def removeChannel(ctx):
    if filter_no_spam.check_black_list(str(ctx.message.author.id)):
        await ctx.reply("you are banned")
        return
    
    data = json.load(open(database))
    if "channel" in data[ctx.guild.name]:
        with open(database, 'w') as db:
            name_channel = data[ctx.guild.name]["channel"]
            del data[ctx.guild.name]["channel"]
            json.dump(data, db)
            
        await ctx.send("channel was delete")
        
        channel = discord.utils.get(ctx.guild.text_channels, name=name_channel)
        await channel.delete()
    else:
        await ctx.send("you don't have a channel")
    


@bot.command()
async def setAnnouncementsChannel(ctx, name_channel):
    if filter_no_spam.check_black_list(str(ctx.message.author.id)):
        await ctx.reply("you are banned")
        return
    
    data = json.load(open(database))
    with open(database, 'w') as db:
        data[ctx.guild.name]["announcementsChannel"] = name_channel
        json.dump(data, db)
        
    channel = discord.utils.get(ctx.guild.text_channels, name=name_channel)
    
    if channel is None:
        await ctx.guild.create_text_channel(name_channel)
        
    await ctx.send("channel was set")
    
    
@bot.command()
async def removeAnnouncementsChannel(ctx):
    if filter_no_spam.check_black_list(str(ctx.message.author.id)):
        await ctx.reply("you are banned")
        return
    
    data = json.load(open(database))
    if "announcementsChannel" in data[ctx.guild.name]:
        with open(database, 'w') as db:
            name_channel = data[ctx.guild.name]["announcementsChannel"]
            del data[ctx.guild.name]["announcementsChannel"]
            json.dump(data, db)
            
        await ctx.send("channel was delete")
        
        channel = discord.utils.get(ctx.guild.text_channels, name=name_channel)
        await channel.delete()
    else:
        await ctx.send("you don't have a channel")
    
    
@bot.command()
async def setPrefixVC(ctx, prefixVC):
    if filter_no_spam.check_black_list(str(ctx.message.author.id)):
        await ctx.reply("you are banned")
        return
    
    data = json.load(open(database))
    with open(database, 'w') as db:
        data[ctx.guild.name]["prefixVC"] = prefixVC
        json.dump(data, db)
        
    await ctx.send("prefix vocal was set")
    

@bot.command()
async def removePrefixVC(ctx):
    if filter_no_spam.check_black_list(str(ctx.message.author.id)):
        await ctx.reply("you are banned")
        return
    
    data = json.load(open(database))
    if "prefixVC" in data[ctx.guild.name]:
        with open(database, 'w') as db:
            del data[ctx.guild.name]["prefixVC"]
            json.dump(data, db)
            
        await ctx.send("prefix vocal was delete")
    else:
        await ctx.send("you don't have a channel")
    

@bot.command()
async def setLang(ctx, new_lang):
    if filter_no_spam.check_black_list(str(ctx.message.author.id)):
        await ctx.reply("you are banned")
        return
    
    data = json.load(open(database))
    with open(database, 'w') as db:
        data[ctx.guild.name]["lang"] = new_lang
        json.dump(data, db)
        
    await ctx.send("new lang was set")
    

@bot.command()
async def helpLang(ctx):
    if filter_no_spam.check_black_list(str(ctx.message.author.id)):
        await ctx.reply("you are banned")
        return
    await ctx.send("all languages code: https://developers.google.com/admin-sdk/directory/v1/languages")
    
    
@bot.command()
async def left(ctx):
    if filter_no_spam.check_black_list(str(ctx.message.author.id)):
        await ctx.reply("you are banned")
        return
    try:
        voice = ctx.guild.voice_client
        await voice.disconnect()
    except:
        await ctx.reply("you are not connected to a voice channel")
        
        

@bot.command()
async def stop(ctx):
    if filter_no_spam.check_black_list(str(ctx.message.author.id)):
        await ctx.reply("you are banned")
        return
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    

@bot.command()
async def spam(ctx, spam):
    if filter_no_spam.check_black_list(str(ctx.message.author.id)):
        await ctx.reply("you are banned")
        return
    
    if spam != "yes" and spam != "no":
        await ctx.reply("use only yes or no")
        return
    
    data = json.load(open(database))
    with open(database, 'w') as db:
        data[ctx.guild.name]["spam"] = spam
        json.dump(data, db)
        
    await ctx.send("spam set")
    

@bot.command()
async def info(ctx):
    await ctx.reply(f'''{ctx.message.author.name}

warns: {filter_no_spam.checkWarns(str(ctx.message.author.id))}/5''')
    
    
#admin
@bot.command()
async def blackList(ctx, id):
    if ctx.message.author.id == 533014724569333770:
        black_list = json.load(open("blacklist.json"))
        with open("blacklist.json", 'w') as bl:
            black_list[id] = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
            json.dump(black_list, bl)
            await ctx.reply("user added of blacklist")
    else:
        await ctx.reply("you don't have permissions to use this command")
        

@bot.command()
async def removeBlackList(ctx, id):
    def check(id, black_list):
        if id in black_list:
            return True
        return False
    
    
    if ctx.message.author.id == 533014724569333770:
        black_list = json.load(open("blacklist.json"))
        if check(id, black_list):
            with open("blacklist.json", 'w') as bl:
                del black_list[id]
                json.dump(black_list, bl)
                await ctx.reply("user removed of blacklist")
        else:
            await ctx.reply("user not found")
            return
    else:
        await ctx.reply("you don't have permissions to use this command")
        

@bot.command()
async def addNoWords(ctx, *, words):
    if ctx.message.author.id == 533014724569333770:
        words = words.replace("\n", " ")
        print(words)
        words = words.split(" ")

        no_words = json.load(open("no_words.json"))
        with open("no_words.json", 'w') as nw:
            for word in words:
                no_words["no_words"].append(word)
                
            json.dump(no_words, nw)
            await ctx.reply("word/words added")
        filter_no_spam.no_words = json.load(open("no_words.json"))["no_words"]
    else:
        await ctx.reply("you don't have permissions to use this command")
        
        
@bot.command()
async def removeNoWords(ctx, *, words):
    def check(word, no_words):
        if word in no_words["no_words"]:
            return True
        return False
    
    
    if ctx.message.author.id == 533014724569333770:
        no_words = json.load(open("no_words.json"))
        words = words.replace("\n", " ")
        words = words.split(" ")
        
        with open("no_words.json", 'w') as nw:
            for word in words:
                if check(word, no_words):
                    no_words["no_words"].remove(word)
                    
            json.dump(no_words, nw)
            await ctx.reply("word/words removed")
        filter_no_spam.no_words = json.load(open("no_words.json"))["no_words"]
    else:
        await ctx.reply("you don't have permissions to use this command")
        

bot.run(token)

