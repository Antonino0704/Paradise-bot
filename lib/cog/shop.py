import discord
from discord.ext import commands
from discord import app_commands

import typing

from lib.spam_lib import Spam
from lib.robux import Robux
from lib.inventory import Inventory
from lib.utils import Utils

from lib.legacy_cog.shop import Shop as LegacyShop

class Shop(LegacyShop, name="Shop"):
    def __init__(self, bot, utils, filter_no_spam, robux, inventory, mysql_connection):
        super().__init__(bot, utils, filter_no_spam, robux, inventory, mysql_connection)
        super().gets_item_icon()

    @app_commands.command(
        name="shop", description="it shown the shop"
    )
    async def shop_slash(self, interaction: discord.Interaction):
        arrow = "<:4596froggyarrow:1011296133131292692>"
        title = f"{interaction.user.name} welcome at shop"
        description = f"""Remove ban: {self.item_list[0]} 40 {arrow} /rban\n
    Change bot activity: {self.item_list[0]} 10 {arrow}  /change-activity\n

    {self.buy_list_create(arrow)}

    Roles for sale in this guild:

    {self.roles_shop_slash(interaction, arrow)}
    """
        embed = discord.Embed(title=title, description=description)
        embed.set_image(url=self.bot.user.avatar)
        await interaction.response.send_message(embed=embed)

    def buy_list_create(self, arrow):
        str_output = ""
        for item in self.mysql_connection.get_item_shop():
            str_output += f"**Get a {item[0].replace('_', ' ')}: {self.item_list[0]} {item[2]}** {arrow} `/Buy`\n"
            str_output += f"**description: {item[1]}**\n\n"
        return str_output
    
    def roles_shop_slash(self, interaction, arrow):
        data = self.mysql_connection.get_role_id_price(interaction.guild_id)
        string = ""
        if data:
            for role in data:
                string += f"<@&{role[0]}> : {self.item_list[0]} {role[1]} {arrow}  /buy-role\n"
            return string
        return None
    
    
    @app_commands.command(
        name="share",
        description="you can share your robux with your friends"    
    )
    @app_commands.describe(user="user who recived robux")
    @app_commands.describe(robux_number="number of robux to give")
    async def share_slash(self, interaction: discord.Interaction, user: discord.Member, robux_number: int):
        ctx = await Utils.getCtx(self.bot, interaction)
        robux_number = robux_number if robux_number >= 0 else -robux_number

        id = str(interaction.user.id)
        pokedex = self.mysql_connection.get_pokedex(id, 1)
        price = robux_number + int((robux_number / 100 * 10))
        price -= self.is_wallet(id, robux_number)

        if pokedex >= price:
            await self.robux.robux(ctx, user.id, robux_number)
            await self.robux.robux(ctx, id, -price)
        else:
            await interaction.response.send_message(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")

        
    @app_commands.command(
        name="rban", description="payment 40 robux to remove from blacklist"
    )
    async def Rban_slash(self, interaction: discord.Interaction):
        ctx = await Utils.getCtx(self.bot, interaction)
        id = str(interaction.user.id)
        pokedex = self.mysql_connection.get_pokedex(id, 1)
        price = 40

        if pokedex >= price:
            if await self.filter_no_spam.remove_black_list(ctx, id):
                await self.robux.payment(ctx, id, price)
        else:
            await interaction.response.send_message(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")

    @app_commands.command(
        name="change-activity", description="payment 10 robux to change activity of the bot"
    )
    @app_commands.describe(game="the game that will be shown in the state")
    async def ChangeActivity_slash(self, interaction: discord.Interaction, game: str):
        id = str(interaction.user.id)
        pokedex = self.mysql_connection.get_pokedex(id, 1)
        price = 10
        game = self.filter_no_spam.censured(game)
        if pokedex >= price:
            await self.bot.change_presence(activity=discord.Game(name=game))
            await self.robux.payment(await Utils.getCtx(self.bot, interaction), id, price)
        else:
            await interaction.response.send_message(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")
    
    async def items(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> typing.List[app_commands.Choice[str]]:
        choices = self.mysql_connection.get_names_item()
        choices.remove("robux")
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices
            if current.lower() in choice.lower()
        ]

    @app_commands.command(
        name="buy", description="you can buy an item"
    )
    @app_commands.autocomplete(item_name=items)
    @app_commands.describe(item_name="item name")
    async def buy(self, interaction: discord.Interaction, item_name: str):
        ctx = await Utils.getCtx(self.bot, interaction)
        id = str(interaction.user.id)

        if self.mysql_connection.is_exist("name", item_name, "items", "item_id"):
            await interaction.response.send_message("sorry we don't have this article yet")
            return
        
        pokedex = self.mysql_connection.get_pokedex(id, 1)
        price = self.mysql_connection.get_item_price(item_name)[0]

        if item_name == "wallet" and not self.mysql_connection.is_exist_composite(
                "user_id", "item_id", id, 5, "pokedex", "amount"
            ):
                await interaction.response.send_messag("you already have a wallet")
                return
        
        if pokedex >= price:
            await self.inventory.buy_object(ctx, id, item_name, 1)
            await self.robux.payment(ctx, id, price)
            return True
        else:
            await interaction.response.send_message(f"<@{id}> doesn't have enough <:robux:1010974169552404551>")
            return False
        
    
    #roles
    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.command(
        name="role-forsale", description="you add role for sale"
    )
    @app_commands.describe(role="role for sale")
    @app_commands.describe(price="the price of role")
    async def addRoleForSale_slash(self, interaction: discord.Interaction, role: discord.Role, price: int):
        try:
            self.mysql_connection.add_role(
                str(role.id), role.name, int(price), interaction.guild_id
            )
            await interaction.response.send_message(f"role added for <:robux:1010974169552404551> {price}")
        except Exception as e:
            await interaction.response.send_message(e)

    
    @app_commands.checks.has_permissions(manage_guild=True) #remove-role-forsale
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.command(
        name="remove-rolesale", description="you remove role for sale"
    )
    @app_commands.describe(role="role for sale")
    async def removeRoleForSale_slash(self, interaction: discord.Interaction, role: discord.Role):
        role_id = str(role.id)

        if not self.mysql_connection.is_exist("role_id", role_id, "roles", "name"):
            try:
                self.mysql_connection.delete_role(role_id)
                await interaction.response.send_message(f"the role has been removed")
                return
            except Exception as e:
                await interaction.response.send_message(e)
                return

        await interaction.response.send_message("the role has not been added to the roles for sale")


    @app_commands.command(
        name="buy-role", description="payment of tot robux chosen by the guild owner to buy roles"
    )
    @app_commands.describe(role="the role you want to buy")
    async def BuyRole_slash(self, interaction: discord.Interaction, role: discord.Role):
        ctx = await Utils.getCtx(self.bot, interaction)
        data = self.mysql_connection.get_role_price(role.id)

        if data:
            id = str(interaction.user.id)
            pokedex = self.mysql_connection.get_pokedex(id, 1)
            price = data - int((data / 100 * 10))
            price += self.is_wallet(str(interaction.guild.owner.id), data)

            if pokedex >= data:
                try:
                    await interaction.user.add_roles(role)
                    await self.robux.robux(ctx, id, -data)
                    await self.robux.robux(ctx, str(interaction.guild.owner.id), price)
                except Exception as e:
                    await interaction.response.send_message(f"error {e}")
            else:
                await interaction.response.send_message(
                    f"<@{id}> doesn't have enough <:robux:1010974169552404551>"
                )
        else:
            await interaction.response.send_message(f"<@&{role.id}> isn't on role for sale")


async def setup(bot, utils, filter_no_spam, robux, inventory, mysql_connection):
    await bot.add_cog(
        Shop(bot, utils, filter_no_spam, robux, inventory, mysql_connection)
    )