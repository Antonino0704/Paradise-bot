import discord
from discord.ext import commands

import json

from lib.spam_lib import Spam
from lib.robux import Robux
from lib.inventory import Inventory

class Shop(commands.Cog, name="Shop"):
    def __init__(self, bot, utils, filter_no_spam, robux, inventory, database, pokedex_db, inventory_db, jobs_db):
        self.bot = bot
        self.utils = utils
        self.filter_no_spam = filter_no_spam
        self.robux = robux
        self.inventory = inventory
        self.database = database
        self.pokedex_db = pokedex_db
        self.inventory_db = inventory_db
        self.jobs_db = jobs_db

    @commands.command()
    async def shop(self, ctx):
        """shown the shop"""

        prefix = json.load(open(self.database))[ctx.guild.name]["prefix"]
        title = f"{ctx.message.author.name} welcome at shop"
        description = f'''Remove ban: <:robux:1010974169552404551> 40 <:4596froggyarrow:1011296133131292692> {prefix}help Rban\n
    Change bot activity: <:robux:1010974169552404551> 10 <:4596froggyarrow:1011296133131292692> {prefix}help ChangeActivity\n
    Adopt a cat: <:robux:1010974169552404551> 5 <:4596froggyarrow:1011296133131292692> {prefix}help AdoptCat\n
    Buy a old house: <:robux:1010974169552404551> 7 <:4596froggyarrow:1011296133131292692> {prefix}help BuyOldHouse\n
    Buy a modern house: <:robux:1010974169552404551> 10 <:4596froggyarrow:1011296133131292692> {prefix}help BuyModernHouse\n
    Buy wallet (one only):  <:robux:1010974169552404551> 20 <:4596froggyarrow:1011296133131292692> {prefix}help BuyWallet

    Roles for sale in this guild:

    {self.roles_shop(ctx, prefix)}
    '''
        embed = discord.Embed(title=title, description=description)
        embed.set_image(url=self.bot.user.avatar_url)
        await ctx.reply(embed=embed)

    def roles_shop(self, ctx, prefix):
        data = json.load(open(self.database))[ctx.guild.name]
        string = ""
        if "roleSale" in data:
            for role in data["roleSale"]:
                string += f"<@&{role}> : <:robux:1010974169552404551> {data['roleSale'][role]} <:4596froggyarrow:1011296133131292692> {prefix}help BuyRole\n"
            return string
        return None

    def is_wallet(self, id, price):
        inventory =  json.load(open(self.inventory_db))
        if id in inventory and "wallet" in inventory[id]:
            return int(price/100*10)
        return 0


    @commands.command()
    async def share(self, ctx, mention_role, robux_number):
        """you can share your robux with your friends, the sender will pay a commission equal to 10% 
            with an approximation of an amount equal to or greater than 10 robux"""

        mention_role = self.utils.mention_replace(mention_role)

        pokedex = json.load(open(self.pokedex_db))
        id = str(ctx.message.author.id)
        robux_number = int(robux_number)
        price = robux_number + int((robux_number/100*10))
        price -= self.is_wallet(id, robux_number)

        if id in pokedex and pokedex[id] >= price:
            await self.robux.robux(ctx, mention_role, robux_number)
            await self.robux.robux(ctx, id, -price)
        else:
            await ctx.reply(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")


    @commands.command()
    async def Rban(self, ctx):
        """payment 40 robux for the remove of the blacklist"""

        pokedex = json.load(open(self.pokedex_db))
        id = str(ctx.message.author.id)
        price = 40
        
        if id in pokedex and pokedex[id] >= price:
            await self.filter_no_spam.remove_black_list(ctx, id)
            await self.robux.payment(ctx, id, pokedex, price)
        else:
            await ctx.reply(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")
            

    @commands.command()
    async def ChangeActivity(self, ctx, game):
        """payment 10 robux for change activity of the bot"""

        pokedex = json.load(open(self.pokedex_db))
        id = str(ctx.message.author.id)
        price = 10
        game = self.filter_no_spam.censured(game)
        if id in pokedex and pokedex[id] >= price:
            await self.bot.change_presence(activity=discord.Game(name=game))
            await self.robux.payment(ctx, id, pokedex, price)
        else:
            await ctx.reply(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")

    
    @commands.command()
    async def AdoptCat(self, ctx):
        """payment 5 robux for adopt a cat"""

        pokedex = json.load(open(self.pokedex_db))
        id = str(ctx.message.author.id)
        price = 5
        
        if id in pokedex and pokedex[id] >= price:
            await self.inventory.buy_object(ctx, id, "cat", 1)
            await self.robux.payment(ctx, id, pokedex, price)
            return True
        else:
            await ctx.reply(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")
            return False


    @commands.command()
    async def BuyOldHouse(self, ctx):
        """payment 7 robux for buy a old house"""

        pokedex = json.load(open(self.pokedex_db))
        id = str(ctx.message.author.id)
        price = 7
        
        if id in pokedex and pokedex[id] >= price:
            await self.inventory.buy_object(ctx, id, "old_house", 1)
            await self.robux.payment(ctx, id, pokedex, price)
            return True
        else:
            await ctx.reply(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")
            return False

    @commands.command()
    async def BuyModernHouse(self, ctx):
        """payment 10 robux for buy a modern house"""

        pokedex = json.load(open(self.pokedex_db))
        id = str(ctx.message.author.id)
        price = 10
        
        if id in pokedex and pokedex[id] >= price:
            await self.inventory.buy_object(ctx, id, "modern_house", 1)
            await self.robux.payment(ctx, id, pokedex, price)
            return True
        else:
            await ctx.reply(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")
            return False


    @commands.command()
    async def BuyWallet(self, ctx):
        """payment 20 robux for buy a wallet, one only, if you buy it you will be absent from commissions by share command"""

        pokedex = json.load(open(self.pokedex_db))
        inventory_data = json.load(open(self.inventory_db))
        id = str(ctx.message.author.id)
        price = 20
        
        if id in pokedex and pokedex[id] >= price:
            if id in inventory_data and "wallet" in inventory_data[id]:
                await ctx.reply("you already have a wallet")
                return

            await self.inventory.buy_object(ctx, id, "wallet", 1)
            await self.robux.payment(ctx, id, pokedex, price)
        else:
            await ctx.reply(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")


    #roles
    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def addRoleForSale(self, ctx, role_id, price):
        """add role for sale, the bot must have permissions to add the role and for every purchase a commission equal to 10% 
            with an approximation of an amount equal to or greater than 10 robux to borne by owner"""
        
        data = json.load(open(self.database))
        if not "roleSale" in data[ctx.guild.name]:
            data[ctx.guild.name]["roleSale"] = {}

        with open(self.database, 'w') as db:
            data[ctx.guild.name]["roleSale"][role_id] = int(price)
            json.dump(data, db)
                
            await ctx.reply(f"role added for <:robux:1010974169552404551> {price}")


    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def removeRoleForSale(self, ctx, role_id):
        """remove role for sale"""
        
        data = json.load(open(self.database))
        if "roleSale" in data[ctx.guild.name] and role_id in data[ctx.guild.name]["roleSale"]:
            with open(self.database, 'w') as db:
                del data[ctx.guild.name]["roleSale"][role_id]
                if len(data[ctx.guild.name]["roleSale"]) == 0:
                    del data[ctx.guild.name]["roleSale"]
                json.dump(data, db)
                    
                await ctx.reply(f"the role <@&{role_id}> has been removed")
                return
        await ctx.reply("the role does not exist or has not been added to the roles for sale")


    @commands.command()
    async def BuyRole(self, ctx, mention_role):
        """payment of tot robux chosen by the guild owner for buy roles"""
        
        data = json.load(open(self.database))[ctx.guild.name]
        mention_role = self.utils.mention_replace(mention_role)

        if "roleSale" in data and mention_role in data["roleSale"]:
            pokedex = json.load(open(self.pokedex_db))
            id = str(ctx.message.author.id)
            price = data["roleSale"][mention_role]  - int((data["roleSale"][mention_role]/100*10))
            price += self.is_wallet(str(ctx.guild.owner.id), data["roleSale"][mention_role])

            if id in pokedex and pokedex[id] >= data["roleSale"][mention_role]:
                try:
                    role = ctx.guild.get_role(int(mention_role))
                    await ctx.message.author.add_roles(role)
                    await self.robux.robux(ctx, id, -data["roleSale"][mention_role])
                    await self.robux.robux(ctx, str(ctx.guild.owner.id), price)
                except Exception as e:
                    await ctx.reply(f"error {e}")
            else:
                await ctx.reply(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")
        else:
             await ctx.reply(f"<@&{mention_role}> isn't on role for sale")


    #event
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.bot.get_user(payload.user_id) == self.bot.user or str(payload.emoji) != "<:robux:1010974169552404551>":
            return
    
        async def points():
            channel = self.bot.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            ctx = await self.bot.get_context(msg)
            if msg.content[22:] == "gives a <:robux:1010974169552404551>, you put the reaction to win it!!" and msg.author == self.bot.user:
                await self.bank(ctx, payload, msg)
                
        await points()

    
    async def bank(self, ctx, payload, msg):
        async def is_banker():
            job = json.load(open(self.jobs_db))
            if str(payload.user_id) in job["banker"]:
                await ctx.send(f"<@{payload.user_id}> you are a banker, you can't get this robux")
                return True
            return False

        async def payment(old_msg):
            job = json.load(open(self.jobs_db))
            old_msg = self.utils.mention_replace(old_msg[:21])
            if old_msg in job["banker"]:
                await self.robux.robux(ctx, old_msg, 2)

        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux) or await is_banker():
            return
             
        old_msg = msg.content
        await msg.clear_reactions()
        await msg.edit(content=f"<@{payload.user_id}> you win")
        await self.robux.robux(ctx, str(payload.user_id), 1)
        await payment(old_msg)