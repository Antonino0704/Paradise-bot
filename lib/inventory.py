import discord

import json


class Inventory:
    def __init__(self):
        self.data_files()

    def data_files(self):
        self.inventory_db = 'jsonFile/inventory.json'

    async def buy_object(self, ctx, id, type_object, num):
        if type_object == "cat":
            await self.type_cat(ctx, id, type_object, num)
        elif type_object == "old_house":
            await self.type_old_house(ctx, id, type_object, num)
        elif type_object == "modern_house":
            await self.type_modern_house(ctx, id, type_object, num)
        elif type_object == "wallet":
            await self.type_wallet(ctx, id, type_object, num) 
        else:
            await ctx.resply("sorry we don't have this article yet")
    
    def is_not_exist(self, id, type_object, inventory):
        if not id in inventory:
            inventory[id] = {}
        if not type_object in inventory[id]:
            inventory[id][type_object] = 0
        return inventory

    async def type_cat(self, ctx, id, type_object, num):
        inventory = json.load(open(self.inventory_db))
        inventory = self.is_not_exist(id, type_object, inventory)

        if num < 0 and inventory[id][type_object] < -num:
            await ctx.reply("you don't have enough cats!! <a:catto:1012052395435499550>")
            return

        with open(self.inventory_db, "w") as ind:
            inventory[id][type_object] += num
            json.dump(inventory, ind)
            await ctx.reply("you have adopt a cat <a:catto:1012052395435499550>")

    async def type_old_house(self, ctx, id, type_object, num):
        inventory = json.load(open(self.inventory_db))
        inventory = self.is_not_exist(id, type_object, inventory)

        if num < 0 and inventory[id][type_object] < -num:
            await ctx.reply("you don't have enough old houses!! <:oldhouse:1012052537198776430>")
            return

        with open(self.inventory_db, "w") as ind:
            inventory[id][type_object] += num
            json.dump(inventory, ind)
            await ctx.reply("you have buy a old house <:oldhouse:1012052537198776430>")

    async def type_modern_house(self, ctx, id, type_object, num):
        inventory = json.load(open(self.inventory_db))
        inventory = self.is_not_exist(id, type_object, inventory)

        if num < 0 and inventory[id][type_object] < -num:
            await ctx.reply("you don't have enough modern houses!! <:modernhouse:1012052596120367236>")
            return

        with open(self.inventory_db, "w") as ind:
            inventory[id][type_object] += num
            json.dump(inventory, ind)
            await ctx.reply("you have buy a modern house <:modernhouse:1012052596120367236>")
    
    async def type_wallet(self, ctx, id, type_object, num):
        inventory = json.load(open(self.inventory_db))
        inventory = self.is_not_exist(id, type_object, inventory)

        if num < 0 and inventory[id][type_object] < -num:
            await ctx.reply("you don't have enough wallet!! <a:wallet:1012053408263438396>")
            return

        with open(self.inventory_db, "w") as ind:
            inventory[id][type_object] += num
            json.dump(inventory, ind)
            await ctx.reply("you have buy a wallet <a:wallet:1012053408263438396>")