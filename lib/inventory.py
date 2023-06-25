import discord

import json


class Inventory:
    def __init__(self, mysql_connection):
        self.mysql_connection = mysql_connection

    async def buy_object(self, ctx, id, type_object, num):
        if self.mysql_connection.is_exist("name", type_object, "items", "item_id"):
            await ctx.resply("sorry we don't have this article yet")
            return

        await self.type_object(ctx, id, type_object, num)

    def is_not_exist(self, id, type_object):
        if self.mysql_connection.is_exist_composite(
            "user_id", "item_id", id, type_object, "pokedex", "amount"
        ):
            if self.mysql_connection.is_exist("user_id", id, "users", "user_id"):
                self.mysql_connection.add_user(id)

            self.mysql_connection.add_item_to_user(id, type_object)

        return self.mysql_connection.get_pokedex(id, type_object)

    async def type_object(self, ctx, id, type_object, num):
        id_object = self.mysql_connection.get_item_price(type_object)[1]
        emoji = self.mysql_connection.get_emoji_icon(id_object)
        amount = self.is_not_exist(id, id_object)
        item_name = self.mysql_connection.get_names_item()

        if num < 0 and amount < -num:
            await ctx.reply(f"you don't have enough {item_name}s!! {emoji}")
            return

        self.mysql_connection.update_pokedex(id, 2, amount + num)
        await ctx.reply(f"you have got {type_object.replace('_', ' ')} {emoji}")

    @DeprecationWarning
    async def type_cat(self, ctx, id, num):
        emoji = self.mysql_connection.get_emoji_icon(2)
        amount = self.is_not_exist(id, 2)

        if num < 0 and amount < -num:
            await ctx.reply(f"you don't have enough cats!! {emoji}")
            return

        self.mysql_connection.update_pokedex(id, 2, amount + num)
        await ctx.reply(f"you have adopt a cat {emoji}")

    @DeprecationWarning
    async def type_old_house(self, ctx, id, num):
        emoji = self.mysql_connection.get_emoji_icon(3)
        amount = self.is_not_exist(id, 3)

        if num < 0 and amount < -num:
            await ctx.reply(f"you don't have enough old houses!! {emoji}")
            return

        self.mysql_connection.update_pokedex(id, 3, amount + num)
        await ctx.reply(f"you have buy a old house {emoji}")

    @DeprecationWarning
    async def type_modern_house(self, ctx, id, num):
        emoji = self.mysql_connection.get_emoji_icon(4)
        amount = self.is_not_exist(id, 4)

        if num < 0 and amount < -num:
            await ctx.reply(f"you don't have enough modern houses!! {emoji}")
            return

        self.mysql_connection.update_pokedex(id, 4, amount + num)
        await ctx.reply(f"you have buy a modern house {emoji}")

    @DeprecationWarning
    async def type_wallet(self, ctx, id, num):
        emoji = self.mysql_connection.get_emoji_icon(5)
        amount = self.is_not_exist(id, 5)

        if num < 0 and amount < -num:
            await ctx.reply(f"you don't have enough wallet!! {emoji}")
            return

        self.mysql_connection.update_pokedex(id, 5, amount + num)
        await ctx.reply(f"you have buy a wallet {emoji}")
