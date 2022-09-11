import json
import random
import discord


class Robux:
    def __init__(self):
        self.data_files()
        self.probably = []
        self.generate_probably()
        
    def data_files(self):
        self.pokedex_db = 'jsonFile/pokedex.json'
        
    def less_one_robux(self, id):
        pokedex = json.load(open(self.pokedex_db))
        if id in pokedex:
            if pokedex[id] > 0:
                with open(self.pokedex_db, "w")as pd:
                    pokedex[id]-=1
                    json.dump(pokedex, pd)
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
                 
    async def payment(self, ctx, id, pokedex, price):
        with open(self.pokedex_db, 'w') as pd:
            pokedex[id] -= price   
            json.dump(pokedex, pd)
            await ctx.reply(f"payment success -{price} <:robux:1010974169552404551> added to <@{id}>")
            
    async def robux(self, ctx, id, robux_number):
        pokedex = json.load(open(self.pokedex_db))
        if not id in pokedex:
            pokedex[id] = 0
            
        if robux_number < 0 and pokedex[id] < -robux_number:
            await ctx.reply(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")
            return
            
        with open(self.pokedex_db, 'w') as pd:
            pokedex[id] += robux_number   
            json.dump(pokedex, pd)
            await ctx.reply(f"{robux_number} <:robux:1010974169552404551> added to <@{id}>")