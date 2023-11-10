import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View

import typing

from lib.utils import Utils
from lib.spam_lib import Spam
from lib.robux import Robux

from lib.legacy_cog.info import Info as LegacyInfo


class Info(LegacyInfo, name="Information"):
    def __init__(self, bot, utils, filter_no_spam, robux, mysql_connection):
        super().__init__(bot, utils, filter_no_spam, robux, mysql_connection)
        super().gets_item_icon()

    async def items(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> typing.List[app_commands.Choice[str]]:
        choices = self.mysql_connection.get_names_item()
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices
            if current.lower() in choice.lower()
        ]

    @app_commands.command(
        name="info-item",
        description="it shows item information",
    )
    @app_commands.autocomplete(item_name=items)
    @app_commands.describe(item_name="item name")
    async def infoItem_slash(self, interaction: discord.Interaction, item_name: str):
        data = self.mysql_connection.get_info("name", item_name, "items")
        if data:
            embed = discord.Embed(title=data[0][0], description=data[0][1])
            return await interaction.response.send_message(embed=embed)
        await interaction.response.send_message("item doesn't exist")

    async def badges(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> typing.List[app_commands.Choice[str]]:
        choices = self.mysql_connection.get_names_badges()
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices
            if current.lower() in choice.lower()
        ]

    @app_commands.command(
        name="info-badge",
        description="it shows badge information",
    )
    @app_commands.autocomplete(badge_name=badges)
    @app_commands.describe(badge_name="badge name")
    async def infoBadge_slash(self, interaction: discord.Interaction, badge_name: str):
        data = self.mysql_connection.get_info("name", badge_name, "badges")
        if data:
            embed = discord.Embed(title=data[0][0], description=data[0][1])
            embed.set_footer(
                text=f"you got that: {self.mysql_connection.get_badge_date(interaction.user.id, badge_name)}"
            )
            return await interaction.response.send_message(embed=embed)
        await interaction.response.send_message("badge doesn't exist")

    async def works(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> typing.List[app_commands.Choice[str]]:
        choices = self.mysql_connection.get_names_jobs()
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices
            if current.lower() in choice.lower()
        ]

    @app_commands.command(
        name="info-job",
        description="it shows job information",
    )
    @app_commands.autocomplete(work_type=works)
    @app_commands.describe(work_type="work type")
    async def infoJob_slash(self, interaction: discord.Interaction, work_type: str):
        data = self.mysql_connection.get_info("name", work_type, "jobs")
        if data:
            embed = discord.Embed(title=data[0][0], description=data[0][1])
            return await interaction.response.send_message(embed=embed)
        await interaction.response.send_message("job doesn't exist")

    @app_commands.command(name="contact-us")
    async def contact_us(self, interaction: discord.Interaction, problem: str):
        for guild in self.bot.guilds:
            if (
                guild.id == 1005889989315416094
            ):  # your personal guild or official bot guild
                user = guild.get_member(533014724569333770)  # your id

        await user.send(problem)
        await interaction.response.send_message(
            f"message sent, we will let you know as soon as possible"
        )

    @app_commands.command(
        name="info",
        description="it shows your warns, robux, inventory and job",
    )
    async def info_slash(self, interaction: discord.Interaction):
        id_s = str(interaction.user.id)
        items = self.mysql_connection.get_pokedex_all(id_s)
        badges = super().getBadge(id_s)
        job = self.mysql_connection.get_user_job(id_s)
        title = str(interaction.user) + badges

        names = self.mysql_connection.get_user_names(id_s, "firstname, lastname")
        names = names[0][0] + " " + names[0][1] if names else "no firstname no lastname"

        description = ""
        for icon, amount in items:
            description += f"""
    {icon}: {amount}\n
            """
        description += f"""
    Job: {job}    
        """

        self.start = 0
        self.finish = 200
        hop = 200

        view = View(timeout=None)
        next_button = Button(
            style=discord.ButtonStyle.green,
            emoji="<a:pinkarrow_right:1172587237628719158>",
        )
        previous_button = Button(
            style=discord.ButtonStyle.green,
            emoji="a:pinkarrow_left:1172587310425055273>",
        )

        def check():
            if (
                len(description) + self.start == len(description)
                and len(description) - self.finish <= 0
            ):
                view.children[0].disabled = True
                view.children[1].disabled = True
            elif len(description) - self.finish <= 0:
                view.children[1].disabled = True
                view.children[0].disabled = False
            elif len(description) + self.start == len(description):
                view.children[0].disabled = True
                view.children[1].disabled = False
            else:
                view.children[0].disabled = False
                view.children[1].disabled = False

        async def next(interaction: discord.Interaction):
            self.start += hop
            self.finish += hop
            embed.description = f"{description[self.start : self.finish]}"

            check()
            await interaction.response.edit_message(embed=embed, view=view)

        async def previous(interaction: discord.Interaction):
            self.start -= hop
            self.finish -= hop
            embed.description = f"{description[self.start : self.finish]}"
            check()
            await interaction.response.edit_message(embed=embed, view=view)

        next_button.callback = next
        previous_button.callback = previous

        view.add_item(previous_button)
        view.add_item(next_button)
        check()
        embed = discord.Embed(
            title=title, description=description[self.start : self.finish]
        )
        embed.set_image(url=interaction.user.avatar)
        embed.set_footer(text=names)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot, utils, filter_no_spam, robux, mysql_connection):
    await bot.add_cog(Info(bot, utils, filter_no_spam, robux, mysql_connection))
