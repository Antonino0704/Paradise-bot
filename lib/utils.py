import json
import random
import discord
from lib.spam_lib import Spam


database = 'database.json'

class Utils:
    def __init__(self):
        self.probably = []
        self.generate_probably()
    
    def get_prefix(self, bot, msg):
        data = json.load(open(database))
        return data[msg.guild.name]["prefix"]
    
    async def is_ban(self, ctx, filter_no_spam):
        if filter_no_spam.check_black_list(str(ctx.message.author.id)):
            if self.less_one_robux(str(ctx.message.author.id)):
                await ctx.reply("-1 <:robux:1010974169552404551>")
                
            await ctx.reply("you are banned")
            return True
        return False
    
    def less_one_robux(self, id):
        data = json.load(open("pokedex.json"))
        if id in data:
            if data[id] > 0:
                with open("pokedex.json", "w")as pd:
                    data[id]-=1
                    json.dump(data, pd)
                    return True
            return False
        return False
    
    def generate_probably(self):
        max = 100
        min = 1
        up = 10
        
        for i in range(100):
            if up == i:
                max += 100
                min += 100
                up += 10
            
            self.probably.append(self.random_number(min, max))
            
    def random_number(self, min, max):
        number = random.randint(min, max)
        for j in self.probably:
            if j == number:
                return self.random_number(min, max)
        return number
                    
    async def catch(self, ctx):
         number = random.randint(1, 1000)
         for i in self.probably:
             if number == i:
                 msg = await ctx.send("<:robux:1010974169552404551> oh a wild robux appeared, you put the reaction to win it!!")
                 await msg.add_reaction("<:robux:1010974169552404551>")
                 
    async def payment(self, ctx, id, data, price):
         with open("pokedex.json", 'w') as pd:
            data[id] -= price   
            json.dump(data, pd)
            await ctx.reply(f"payment success -{price} <:robux:1010974169552404551> added to <@{id}>")
        