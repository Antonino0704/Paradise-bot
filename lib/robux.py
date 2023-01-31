import json
import random
import discord


class Robux:
    def __init__(self, mysql_connection):
        self.probably = []
        self.generate_probably()
        self.mysql_connection = mysql_connection
        self.emoji = mysql_connection.get_emoji_icon(1)
        
    def less_one_robux(self, id):
        amount = self.mysql_connection.get_pokedex(id, 1)
        if amount > 0:
            self.mysql_connection.update_pokedex(id, 1, amount-1)
            return True
        return False
    
    def generate_probably(self):
        max = 100
        min = 1
        up = 1  #first it was 10
        
        for i in range(10):  #range was 100
            if up == i:
                max += 100
                min += 100
                up += 1  #up was 10
            
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
                msg = await ctx.send(f"{self.emoji} oh! a wild robux appeared, use the reaction to win it!!")
                await msg.add_reaction(self.emoji)
                 
    async def payment(self, ctx, id, price):
        amount = self.mysql_connection.get_pokedex(id, 1)
        self.mysql_connection.update_pokedex(id, 1, amount-price)
        await ctx.reply(f"payment success -{price} {self.emoji} added to <@{id}>")
            
    async def robux(self, ctx, id, robux_number):
        if self.mysql_connection.is_exist_composite("user_id", "item_id", id, 1, "pokedex", "amount"):
            if self.mysql_connection.is_exist("user_id", id, "users", "user_id"):
                self.mysql_connection.add_user(id)
                
            self.mysql_connection.add_item_to_user(id, 1)

        amount = self.mysql_connection.get_pokedex(id, 1)

        if robux_number < 0 and amount < -robux_number:
            await ctx.reply(f"<@{id}> doesn't have enough {self.emoji}")
            return
            
        self.mysql_connection.update_pokedex(id, 1, amount+robux_number)
        await ctx.reply(f"{robux_number} {self.emoji} added to <@{id}>")
