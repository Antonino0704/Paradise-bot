import json
import random
import asyncio

class Jobs:
    def __init__(self):
        self.data_files()
        self.work = ""

    def data_files(self):
        self.jobs_db = 'jsonFile/jobs.json'

    def already_job(self, id):
        job = json.load(open(self.jobs_db))
        if not id in job["criminal"] and not id in job["banker"]:
            return False
        return True

    def check_worker(self, id):
        job = json.load(open(self.jobs_db))[self.work]
        if not id in job:
            return False
        return True

    def add_worker(self, id):
        job = json.load(open(self.jobs_db))
        if not self.already_job(id):
            with open(self.jobs_db, "w") as jbd:
                job[self.work][id] = 1
                json.dump(job, jbd)
            return f"the {self.work} job is yours"
        return f"already you have a job"

    def remove_worker(self, id):
        job = json.load(open(self.jobs_db))
        if self.check_worker(id):
            with open(self.jobs_db, "w") as jbd:
                del job[self.work][id]
                json.dump(job, jbd)
            return f"you lost the {self.work} job"
        return f"you don't have {self.work} job"

    def working(self, *args):
        pass


class Criminal(Jobs):
    def __init__(self):
        super().__init__()
        self.work = "criminal"
        self.inventory_db = 'jsonFile/inventory.json'
        self.money = 0

    async def working(self, ctx, criminal_id, victim_id, robux):
        try:
            number = random.randint(1, 1000)
            
            for i in robux.probably:
                if number == i:
                    pokedex = json.load(open(robux.pokedex_db))
                    self.money = int(pokedex[victim_id]/100*10)
                    self.house(victim_id)
                    await asyncio.sleep(30+self.money)
                    await robux.robux(ctx, victim_id, -self.money)
                    await robux.robux(ctx, criminal_id, self.money)
        except KeyError:
            pass
        await self.feedback(ctx)

    def house(self, victim_id):
        inventory = json.load(open(self.inventory_db))
        
        if victim_id in inventory:
            if "old_house" in inventory[victim_id]:
                for _ in range(inventory[victim_id]["old_house"]):
                    self.money -= 5
            if "modern_house" in inventory[victim_id]:
                for _ in range(inventory[victim_id]["modern_house"]):
                    self.money -= 10    
        return self.money

    async def feedback(self, ctx):
        if self.money == 0:
            await ctx.reply("you failed")
            return
        await ctx.reply("you win")


class Banker(Jobs):
    def __init__(self):
        super().__init__()
        self.work = "banker"

    async def working(self, ctx):
        await asyncio.sleep(600)
        msg = await ctx.send(f"<@{ctx.message.author.id}> drops a <:robux:1010974169552404551>, you put the reaction to win it!!")
        await msg.add_reaction("<:robux:1010974169552404551>")


class PetSeller(Jobs):
    def __init__(self):
        super().__init__()
        self.work = "petSeller"

    async def working(self, ctx):
        await asyncio.sleep(300)
        msg = await ctx.send(f"<@{ctx.message.author.id}> sale a <a:catto:1012052395435499550>, you put the reaction to buy it <:robux:1010974169552404551> 3!!")
        await msg.add_reaction("<a:catto:1012052395435499550>")
    