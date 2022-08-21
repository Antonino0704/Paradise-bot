import json
import random
import discord


database = 'database.json'

class Utils:
    def __init__(self):
        self.probably = []
        self.generate_probably()
    
    def get_prefix(self, bot, msg):
        data = json.load(open(database))
        return data[msg.guild.name]["prefix"]
    
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
        