import discord
from discord.ext import commands

import json

from lib.spam_lib import Spam
from lib.robux import Robux
from lib.inventory import Inventory


class Shop(commands.Cog, name="Shop"):
    def __init__(self, bot, utils, filter_no_spam, robux, inventory, mysql_connection):
        self.bot = bot
        self.utils = utils
        self.filter_no_spam = filter_no_spam
        self.robux = robux
        self.inventory = inventory
        self.mysql_connection = mysql_connection
        self.gets_item_icon()

    def gets_item_icon(self):
        self.item_list = self.utils.gets_item_icon()

    # PendingDeprecationWarning
    @commands.command()
    async def shop(self, ctx):
        """⚠ This command is deprecated, instead use /shop ⚠
        shown the shop"""

        prefix = self.mysql_connection.get_guild_data(ctx.guild.id, "prefix")
        arrow = "<:4596froggyarrow:1011296133131292692>"
        title = f"{ctx.message.author.name} welcome at shop"
        description = f"""Remove ban: {self.item_list[0]} 40 {arrow} {prefix}help Rban\n
    Change bot activity: {self.item_list[0]} 10 {arrow} {prefix}help ChangeActivity\n
    Adopt a cat: {self.item_list[0]} 5 {arrow} {prefix}help AdoptCat\n
    Buy a old house: {self.item_list[0]} 7 {arrow} {prefix}help BuyOldHouse\n
    Buy a modern house: {self.item_list[0]} 10 {arrow} {prefix}help BuyModernHouse\n
    Buy wallet (one only):  {self.item_list[0]} 20 {arrow} {prefix}help BuyWallet

    Roles for sale in this guild:

    {self.roles_shop(ctx, prefix, arrow)}
    """
        embed = discord.Embed(title=title, description=description)
        embed.set_image(url=self.bot.user.avatar)
        await ctx.reply(embed=embed)

    # PendingDeprecationWarning
    def roles_shop(self, ctx, prefix, arrow):
        data = self.mysql_connection.get_role_id_price(ctx.guild.id)
        string = ""
        if data:
            for role in data:
                string += f"<@&{role[0]}> : {self.item_list[0]} {role[1]} {arrow} {prefix}help BuyRole\n"
            return string
        return None

    def is_wallet(self, id, price):
        if not self.mysql_connection.is_exist_composite(
            "user_id", "item_id", id, "5", "pokedex", "amount"
        ):
            return int(price / 100 * 10)
        return 0

    # PendingDeprecationWarning
    @commands.command()
    async def share(self, ctx, mention_role, robux_number):
        """⚠ This command is deprecated, instead use /share ⚠
        you can share your robux with your friends, the sender will pay a commission equal to 10%
        with an approximation of an amount equal to or greater than 10 robux"""

        robux_number = int(robux_number)
        robux_number = robux_number if robux_number >= 0 else -robux_number
        mention_role = self.utils.mention_replace(mention_role)

        id = str(ctx.message.author.id)
        pokedex = self.mysql_connection.get_pokedex(id, 1)
        robux_number = int(robux_number)
        price = robux_number + int((robux_number / 100 * 10))
        price -= self.is_wallet(id, robux_number)

        if pokedex >= price:
            await self.robux.robux(ctx, mention_role, robux_number)
            await self.robux.robux(ctx, id, -price)
        else:
            await ctx.reply(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")

    # PendingDeprecationWarning
    @commands.command()
    async def Rban(self, ctx):
        """⚠ This command is deprecated, instead use /rban ⚠
        payment 40 robux to remove from blacklist"""

        id = str(ctx.message.author.id)
        pokedex = self.mysql_connection.get_pokedex(id, 1)
        price = 40

        if pokedex >= price:
            if await self.filter_no_spam.remove_black_list(ctx, id):
                await self.robux.payment(ctx, id, price)
        else:
            await ctx.reply(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")

    # PendingDeprecationWarning
    @commands.command()
    async def ChangeActivity(self, ctx, game):
        """⚠ This command is deprecated, instead use /change-activity ⚠
        payment 10 robux to change activity of the bot"""

        id = str(ctx.message.author.id)
        pokedex = self.mysql_connection.get_pokedex(id, 1)
        price = 10
        game = self.filter_no_spam.censured(game)
        if pokedex >= price:
            await self.bot.change_presence(activity=discord.Game(name=game))
            await self.robux.payment(ctx, id, price)
        else:
            await ctx.reply(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")

    # PendingDeprecationWarning
    @commands.command()
    async def AdoptCat(self, ctx):
        """⚠ This command is deprecated, instead use /buy ⚠
        payment 5 robux to adopt a cat"""

        id = str(ctx.message.author.id)
        pokedex = self.mysql_connection.get_pokedex(id, 1)
        price = 5

        if pokedex >= price:
            await self.inventory.buy_object(ctx, id, "cat", 1)
            await self.robux.payment(ctx, id, price)
            return True
        else:
            await ctx.reply(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")
            return False

    # PendingDeprecationWarning
    @commands.command()
    async def BuyOldHouse(self, ctx):
        """⚠ This command is deprecated, instead use /buy ⚠
        payment 7 robux to buy a old house"""

        id = str(ctx.message.author.id)
        pokedex = self.mysql_connection.get_pokedex(id, 1)
        price = 7

        if pokedex >= price:
            await self.inventory.buy_object(ctx, id, "old_house", 1)
            await self.robux.payment(ctx, id, price)
            return True
        else:
            await ctx.reply(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")
            return False

    # PendingDeprecationWarning
    @commands.command()
    async def BuyModernHouse(self, ctx):
        """⚠ This command is deprecated, instead use /buy ⚠
        payment 10 robux to buy a modern house"""

        id = str(ctx.message.author.id)
        pokedex = self.mysql_connection.get_pokedex(id, 1)
        price = 10

        if pokedex >= price:
            await self.inventory.buy_object(ctx, id, "modern_house", 1)
            await self.robux.payment(ctx, id, price)
            return True
        else:
            await ctx.reply(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")
            return False

    # PendingDeprecationWarning
    @commands.command()
    async def BuyWallet(self, ctx):
        """⚠ This command is deprecated, instead use /buy ⚠
        payment 20 robux to buy a wallet, one only, if you buy it you will be absent from commissions by share command"""

        id = str(ctx.message.author.id)
        pokedex = self.mysql_connection.get_pokedex(id, 1)
        price = 20

        if pokedex >= price:
            if not self.mysql_connection.is_exist_composite(
                "user_id", "item_id", id, 5, "pokedex", "amount"
            ):
                await ctx.reply("you already have a wallet")
                return

            await self.inventory.buy_object(ctx, id, "wallet", 1)
            await self.robux.payment(ctx, id, price)
        else:
            await ctx.reply(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")

    # roles

    # PendingDeprecationWarning
    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def addRoleForSale(self, ctx, name_role, price, hex_color="0x00ff00"):
        """"⚠ This command is deprecated, instead use /role-forsale ⚠
        you add role for sale, the bot must have permissions to add the role and for every purchase a commission equal to 10%
        with an approximation of an amount equal to or greater than 10 robux to borne by owner
        """

        try:
            role = discord.utils.get(ctx.guild.roles, name=name_role)

            if role is None:
                role = await ctx.guild.create_role(
                    name=name_role, colour=int(hex_color, 16)
                )

            self.mysql_connection.add_role(
                str(role.id), name_role, int(price), ctx.guild.id
            )
            await ctx.reply(f"role added for <:robux:1010974169552404551> {price}")
        except Exception as e:
            await ctx.reply(e)

    # PendingDeprecationWarning
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def removeRoleForSale(self, ctx, name_role):
        """⚠ This command is deprecated, instead use /remove-rolesale ⚠
        you remove role for sale"""

        role = discord.utils.get(ctx.guild.roles, name=name_role)
        if role is None:
            await ctx.reply("the role doesn't exist")
            return
        role_id = str(role.id)

        if not self.mysql_connection.is_exist("role_id", role_id, "roles", "name"):
            try:
                await role.delete()
                self.mysql_connection.delete_role(role_id)
                await ctx.reply(f"the role has been removed")
                return
            except Exception as e:
                await ctx.reply(e)
                return

        await ctx.reply("the role has not been added to the roles for sale")

    # PendingDeprecationWarning
    @commands.command()
    async def BuyRole(self, ctx, mention_role):
        """⚠ This command is deprecated, instead use /buy-role ⚠
        payment of tot robux chosen by the guild owner to buy roles"""

        mention_role = self.utils.mention_replace(mention_role)
        data = self.mysql_connection.get_role_price(mention_role)

        if data:
            id = str(ctx.message.author.id)
            pokedex = self.mysql_connection.get_pokedex(id, 1)
            price = data - int((data / 100 * 10))
            price += self.is_wallet(str(ctx.guild.owner.id), data)

            if pokedex >= data:
                try:
                    role = ctx.guild.get_role(int(mention_role))
                    await ctx.message.author.add_roles(role)
                    await self.robux.robux(ctx, id, -data)
                    await self.robux.robux(ctx, str(ctx.guild.owner.id), price)
                except Exception as e:
                    await ctx.reply(f"error {e}")
            else:
                await ctx.reply(
                    f"<@{id}> doesn't have enough <:robux:1010974169552404551>"
                )
        else:
            await ctx.reply(f"<@&{mention_role}> isn't on role for sale")

    # event
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if (
            self.bot.get_user(payload.user_id) == self.bot.user
            or not str(payload.emoji) in self.item_list
        ):
            return

        async def points():
            channel = self.bot.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            ctx = await self.bot.get_context(msg)
            if (
                msg.content[22:]
                == f"drops a {self.item_list[0]}, you put the reaction to win it!!"
                and msg.author == self.bot.user
            ):
                await self.bank(ctx, payload, msg)

            if (
                msg.content[22:]
                == f"sales a {self.item_list[1]}, you put the reaction to buy it <:robux:1010974169552404551> 3!!"
                and msg.author == self.bot.user
            ):
                await self.petSell(ctx, payload, msg)

        await points()

    async def bank(self, ctx, payload, msg):
        async def is_banker():
            if not self.mysql_connection.is_exist_composite(
                "user_id", "work_id", str(payload.user_id), "1", "users", "work_id"
            ):
                await ctx.send(
                    f"<@{payload.user_id}>, you are a banker, you can't get this robux"
                )
                return True
            return False

        async def payment(old_msg):
            old_msg = self.utils.mention_replace(old_msg[:21])
            if not self.mysql_connection.is_exist_composite(
                "user_id", "work_id", str(old_msg), "1", "users", "work_id"
            ):
                await self.robux.robux(ctx, old_msg, 2)

        if (
            await self.utils.is_ban(ctx, self.filter_no_spam, self.robux)
            or await is_banker()
        ):
            return

        old_msg = msg.content
        await msg.clear_reactions()
        await msg.edit(content=f"<@{payload.user_id}> you win")
        await self.robux.robux(ctx, str(payload.user_id), 1)
        await payment(old_msg)

    async def petSell(self, ctx, payload, msg):
        async def is_petSeller():
            if not self.mysql_connection.is_exist_composite(
                "user_id", "work_id", str(payload.user_id), 3, "users", "work_id"
            ):
                await ctx.send(
                    f"<@{payload.user_id}>, you are a pet seller, you can't get this cat"
                )
                return True
            return False

        async def payment():
            id = str(payload.user_id)
            pokedex = self.mysql_connection.get_pokedex(id, 1)
            if pokedex >= 3:
                await self.inventory.buy_object(ctx, id, "cat", 1)
                await self.robux.payment(ctx, str(payload.user_id), 3)
                return True
            await ctx.reply(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")
            return False

        async def payment_seller(old_msg):
            old_msg = self.utils.mention_replace(old_msg[:21])
            if not self.mysql_connection.is_exist_composite(
                "user_id", "work_id", str(old_msg), 3, "users", "work_id"
            ):
                cat = self.mysql_connection.get_pokedex(old_msg, 2)
                price = 3 * cat
                price -= int((price / 100 * 10))
                price += self.is_wallet(old_msg, 3 * cat)

                await self.robux.robux(ctx, old_msg, price)

        if (
            await self.utils.is_ban(ctx, self.filter_no_spam, self.robux)
            or await is_petSeller()
        ):
            return

        if await payment():
            old_msg = msg.content
            await msg.clear_reactions()
            await msg.edit(content=f"<@{payload.user_id}> bought it")
            await payment_seller(old_msg)


async def setup(bot, utils, filter_no_spam, robux, inventory, mysql_connection):
    await bot.add_cog(
        Shop(bot, utils, filter_no_spam, robux, inventory, mysql_connection)
    )
