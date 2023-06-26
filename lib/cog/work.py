import json
import discord
from discord.ext import commands
from discord import app_commands

import typing

from lib.utils import Utils
from lib.spam_lib import Spam
from lib.robux import Robux
from lib.jobs import Criminal, Banker, PetSeller
from lib.cog.events import Events

from lib.legacy_cog.work import Work as LegacyWork


class Work(LegacyWork, name="Jobs"):
    def __init__(self, bot, utils, filter_no_spam, robux, mysql_connection):
        super().__init__(bot, utils, filter_no_spam, robux, mysql_connection)

    async def works(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> typing.List[app_commands.Choice[str]]:
        choices = ["criminal", "banker", "petSeller"]
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices
            if current.lower() in choice.lower()
        ]

    @app_commands.command(name="make-request", description="you get a job")
    @app_commands.autocomplete(work_type=works)
    @app_commands.describe(work_type="what job you want to do")
    async def makeRequest_slash(self, interaction: discord.Interaction, work_type: str):
        """
        required:
        criminal: >10 and <50 robux
        banker: >= 50 robux
        pet seller: 1 cat"""

        if await self.utils.is_ban(
            await Utils.getCtx(self.bot, interaction), self.filter_no_spam, self.robux
        ):
            return

        id = str(interaction.user.id)
        robux = self.mysql_connection.get_pokedex(id, 1)
        cat = self.mysql_connection.get_pokedex(id, 2)

        if robux:
            if work_type == "criminal" and robux >= 10 and robux < 50:
                await interaction.response.send_message(self.criminal.add_worker(id))
                return

            elif work_type == "banker" and robux >= 50:
                await interaction.response.send_message(
                    self.banker.add_worker(str(interaction.user.id))
                )
                return

        if cat:
            if work_type == "petSeller":
                await interaction.response.send_message(
                    self.petSeller.add_worker(str(interaction.user.id))
                )
                return

        await interaction.response.send_message(
            "work type doesn't exist or you don't have required"
        )

    @app_commands.command(name="resignation", description="you lose your current job")
    async def resignation_slash(self, interaction: discord.Interaction):
        id = str(interaction.user.id)
        if self.criminal.check_worker(id):
            await interaction.response.send_message(self.criminal.remove_worker(id))

        elif self.banker.check_worker(id):
            await interaction.response.send_message(self.banker.remove_worker(id))

        elif self.petSeller.check_worker(id):
            await interaction.response.send_message(self.petSeller.remove_worker(id))

        else:
            await interaction.response.send_message("you don't have a job")

    @app_commands.command(
        name="steal",
        description="you can steal with 10% of probability the 10% of user's assets",
    )
    @app_commands.describe(victim="the victim")
    async def steal_slash(
        self, interaction: discord.Interaction, victim: discord.Member
    ):
        """you can steal with 10% of probability the 10% of user's assets

        if the user has houses, -5 for all old house and -10 for all modern house, the result will be your salary

        you can use the command every 30 seconds + the salary in seconds (ex. 3 robux are 3 seconds)
        """

        ctx = await Utils.getCtx(self.bot, interaction)
        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return

        id = str(interaction.user.id)
        if self.criminal.check_worker(id):
            await self.criminal.working(ctx, id, victim.id, self.robux)
        else:
            await interaction.response.send_message("you aren't a criminal")

    @app_commands.command(
        name="print-robux",
        description="you can drop a robux, who puts reaction it gets 1 robux, while the banker gets 2 robux",
    )
    async def printRobux_slash(self, interaction: discord.Interaction):
        """you can use the command every 10 minutes"""

        ctx = await Utils.getCtx(self.bot, interaction)
        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return

        id = str(interaction.user.id)
        if self.banker.check_worker(id):
            await self.banker.working(ctx)
        else:
            await interaction.response.send_message("you aren't a banker")

    @app_commands.command(
        name="sale-cat",
        description="you can sale a cat, who puts the reaction pays 3 robux for a cat, while pet seller gets 3 robux",
    )
    async def saleCat_slash(self, interaction: discord.Interaction):
        """
        the salary will multiply for each cat
        if you go over 9 robux will be applicate the taxs, wallet's power is applicable

        you can use the command every 5 minutes"""

        ctx = await Utils.getCtx(self.bot, interaction)
        if await self.utils.is_ban(ctx, self.filter_no_spam, self.robux):
            return

        id = str(interaction.user.id)
        if self.petSeller.check_worker(id):
            await self.petSeller.working(ctx)
        else:
            await interaction.response.send_message("you aren't a pet seller")


async def setup(bot, utils, filter_no_spam, robux, mysql_connection):
    await bot.add_cog(Work(bot, utils, filter_no_spam, robux, mysql_connection))
