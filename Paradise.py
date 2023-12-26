from discord import *
from discord.ext import commands
import discord.utils

from gtts import gTTS
from dotenv import load_dotenv
import json
import os
import asyncio

from lib.utils import Utils
from lib.spam_lib import Spam
from lib.robux import Robux
from lib.inventory import Inventory
from lib.jobs import *
from lib.mysql import Mysql

from lib.cog.admin import Admin
from lib.cog.initSettings import InitSettings
from lib.cog.shop import Shop
from lib.cog.info import Info
from lib.cog.managerVC import ManagerVC
from lib.cog.work import Work
from lib.cog.events import Events
from lib.cog.noCategory import noCategory
from lib.cog.developer import Developer


load_dotenv()
token = os.environ["token"]

intents = discord.Intents.all()
intents.members = True
intents.presences = True

mysql_connection = Mysql(os.environ["address"], os.environ["usr"], os.environ["passwd"])
utils = Utils(mysql_connection)
filter_no_spam = Spam(mysql_connection)
robux = Robux(mysql_connection)
inventory = Inventory(mysql_connection)

queue = {}

bot = commands.Bot(command_prefix=(utils.get_prefix), intents=intents)


def queue_init(id):
    queue[id] = {}
    queue[id]["content"] = []
    queue[id]["status"] = False


@bot.event
async def on_ready():
    print("I'm ready")
    await bot.tree.sync()
    for guild in bot.guilds:
        queue_init(guild.id)
        print(f"guild's name: {guild.name}, owner: {guild.owner}")


@bot.event
async def on_guild_join(guild):
    mysql_connection.guild_join(guild.id, utils.remove_emoji(guild.name))
    queue_init(guild.id)


@bot.event
async def on_guild_update(before, after):
    if before.name != after.name:
        mysql_connection.update_guild_data(
            before.id, "name", utils.remove_emoji(after.name)
        )


async def load_cogs():
    # cog
    await bot.add_cog(Admin(bot, filter_no_spam, robux, inventory, mysql_connection))

    await bot.add_cog(InitSettings(bot, utils, filter_no_spam, robux, mysql_connection))

    await bot.add_cog(
        Shop(bot, utils, filter_no_spam, robux, inventory, mysql_connection)
    )

    await bot.add_cog(Info(bot, utils, filter_no_spam, robux, mysql_connection))

    await bot.add_cog(
        ManagerVC(
            bot,
            os.environ["songs"],
            os.environ["ffmpeg"],
            utils,
            filter_no_spam,
            robux,
            queue,
            mysql_connection,
        )
    )

    await bot.add_cog(Work(bot, utils, filter_no_spam, robux, mysql_connection))

    await bot.add_cog(Events(bot, utils, filter_no_spam, robux, mysql_connection))

    await bot.add_cog(noCategory(bot, utils, filter_no_spam, robux, mysql_connection))

    await bot.add_cog(Developer(bot, mysql_connection))


async def main():
    await load_cogs()
    await bot.start(token)


asyncio.run(main())
