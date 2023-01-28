import json
import random
import asyncio

class Jobs:
    def __init__(self, mysql_connection):
        self.work = ""
        self.mysql_connection = mysql_connection

    def already_job(self, id):
        if not self.mysql_connection.is_exist("user_id", id, "users", "work_id"):
            return True
        return False

    def check_worker(self, id):
        work_id = self.mysql_connection.get_work_by_name(self.work)
        if self.mysql_connection.is_exist_composite("user_id", "work_id", id, work_id, "users", "work_id"):
            return False
        return True

    def add_worker(self, id):
        if not self.already_job(id):
            work_id = self.mysql_connection.get_work_by_name(self.work)
            self.mysql_connection.update_work(id, work_id)
            return f"the {self.work} job is yours"
        return f"already you have a job"

    def remove_worker(self, id):
        if self.check_worker(id):
            self.mysql_connection.update_work(id, None)
            return f"you lost the {self.work} job"
        return f"you don't have {self.work} job"

    def working(self, *args):
        pass


class Criminal(Jobs):
    def __init__(self, mysql_connection):
        super().__init__(mysql_connection)
        self.work = "criminal"
        self.money = 0

    async def working(self, ctx, criminal_id, victim_id, robux):
        try:
            number = random.randint(1, 1000)
            
            for i in robux.probably:
                if number == i:
                    self.money = self.mysql_connection.get_pokedex(victim_id, 1) / 100 * 1
                    self.house(victim_id)
                    await ctx.send(f"wait {30+self.money} seconds")
                    await asyncio.sleep(30+self.money)
                    await robux.robux(ctx, victim_id, -self.money)
                    await robux.robux(ctx, criminal_id, self.money)
        except KeyError:
            pass
        await self.feedback(ctx)

    def house(self, victim_id):
        old_house = self.mysql_connection.get_pokedex(victim_id, 2)
        modern_house = self.mysql_connection.get_pokedex(victim_id, 3)
        if old_house:
            self.money -= 5 * old_house
        if modern_house:
            self.money -= 10 * old_house
                    
        self.money = 0 if self.money < 0 else self.money 
        return self.money

    async def feedback(self, ctx):
        if self.money == 0:
            await ctx.reply("you failed")
            return
        await ctx.reply("you win")


class Banker(Jobs):
    def __init__(self, mysql_connection):
        super().__init__(mysql_connection)
        self.work = "banker"

    async def working(self, ctx):
        await ctx.send("wait 10 minutes")
        await asyncio.sleep(600)
        emoji_icon = self.mysql_connection.get_emoji_icon(1)
        msg = await ctx.send(f"<@{ctx.message.author.id}> drops a {emoji_icon}, you put the reaction to win it!!")
        await msg.add_reaction(emoji_icon)


class PetSeller(Jobs):
    def __init__(self, mysql_connection):
        super().__init__(mysql_connection)
        self.work = "petSeller"

    async def working(self, ctx):
        await ctx.send("wait 5 minutes")
        await asyncio.sleep(300)
        emoji_robux = self.mysql_connection.get_emoji_icon(1)
        emoji_catto = self.mysql_connection.get_emoji_icon(2)
        msg = await ctx.send(f"<@{ctx.message.author.id}> sales a {emoji_catto}, you put the reaction to buy it {emoji_robux} 3!!")
        await msg.add_reaction(emoji_catto)
    