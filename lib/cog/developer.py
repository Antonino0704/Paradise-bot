import discord
from discord.ext import commands
from discord import app_commands


class Developer(commands.Cog, name="Developer"):
    def __init__(self, bot, mysql_connection):
        self.bot = bot
        self.mysql_connection = mysql_connection

    async def passDevbeloperCheck(self, interaction: discord.Interaction) -> bool:
        DEVELOPER_PRIVILEGE = self.mysql_connection.check_privileges(
            str(interaction.user.id), 2
        )
        if not DEVELOPER_PRIVILEGE:
            await interaction.response.send_message(
                "You don't have permission to use this command"
            )
            return False
        return True

    @app_commands.command(
        name="users-badges",
        description="how many users have badges",
    )
    async def usersBadges(self, interaction: discord.Interaction):
        if await self.passDevbeloperCheck(interaction):
            result = self.mysql_connection.users_badges_list()
            embed = discord.Embed(
                title="Results",
            )
            for column in result:
                embed.add_field(
                    name=f"**{column[0]}**",
                    value=f"> Users: {column[1]}\n",
                    inline=False,
                )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="users-items",
        description="how many users have items",
    )
    async def usersItems(self, interaction: discord.Interaction):
        if await self.passDevbeloperCheck(interaction):
            result = self.mysql_connection.users_items_list()
            embed = discord.Embed(
                title="Results",
            )
            for column in result:
                embed.add_field(
                    name=f"**{column[0]}**",
                    value=f"> Users: {column[1]}\n",
                    inline=False,
                )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="count-items",
        description="how many items there are",
    )
    async def howItems(self, interaction: discord.Interaction):
        if await self.passDevbeloperCheck(interaction):
            result = self.mysql_connection.how_items_list()
            embed = discord.Embed(
                title="Results",
            )
            for column in result:
                embed.add_field(
                    name=f"**{column[0]}**",
                    value=f"> Quantity: {column[1]}\n",
                    inline=False,
                )
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot, mysql_connection):
    await bot.add_cog(Developer(bot, mysql_connection))
