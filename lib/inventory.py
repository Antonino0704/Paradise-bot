import discord

import json


class Inventory:
    def __init__(self, mysql_connection):
        self.mysql_connection = mysql_connection

    async def buy_object(self, ctx, id, type_object, num):
        if type_object == "cat":
            await self.type_cat(ctx, id, num)
        elif type_object == "old_house":
            await self.type_old_house(ctx, id, num)
        elif type_object == "modern_house":
            await self.type_modern_house(ctx, id, num)
        elif type_object == "wallet":
            await self.type_wallet(ctx, id, num) 
        else:
            await ctx.resply("sorry we don't have this article yet")
    
    def is_not_exist(self, id, type_object):
        if self.mysql_connection.is_exist_composite("user_id", "item_id", id, type_object, "pokedex", "amount"):
            if self.mysql_connection.is_exist("user_id", id, "users", "user_id"):
                self.mysql_connection.add_user(id)
                
            self.mysql_connection.add_item_to_user(id, type_object)

        return self.mysql_connection.get_pokedex(id, type_object)

    async def type_cat(self, ctx, id, num):
        emoji = self.mysql_connection.get_emoji_icon(2)
        amount = self.is_not_exist(id, 2)

        if num < 0 and amount < -num:
            await ctx.reply(f"you don't have enough cats!! {emoji}")
            return
        
        self.mysql_connection.update_pokedex(id, 2, amount+num)
        await ctx.reply(f"you have adopt a cat {emoji}")

    async def type_old_house(self, ctx, id, num):
        emoji = self.mysql_connection.get_emoji_icon(3)
        amount = self.is_not_exist(id, 3)

        if num < 0 and amount < -num:
            await ctx.reply(f"you don't have enough old houses!! {emoji}")
            return

        self.mysql_connection.update_pokedex(id, 3, amount+num)
        await ctx.reply(f"you have buy a old house {emoji}")

    async def type_modern_house(self, ctx, id, num):
        emoji = self.mysql_connection.get_emoji_icon(4)
        amount = self.is_not_exist(id, 4)

        if num < 0 and amount < -num:
            await ctx.reply(f"you don't have enough modern houses!! {emoji}")
            return

        self.mysql_connection.update_pokedex(id, 4, amount+num)
        await ctx.reply(f"you have buy a modern house {emoji}")
    
    async def type_wallet(self, ctx, id, num):
        emoji = self.mysql_connection.get_emoji_icon(5)
        amount = self.is_not_exist(id, 5)

        if num < 0 and amount < -num:
            await ctx.reply(f"you don't have enough wallet!! {emoji}")
            return

        self.mysql_connection.update_pokedex(id, 5, amount+num)
        await ctx.reply(f"you have buy a wallet {emoji}")