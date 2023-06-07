import json
import datetime
from lib.mysql import Mysql


class Spam:
    def __init__(self, mysql_connection):
        # self.no_spam = {}
        self.mysql_connection = mysql_connection
        # self.msg_stopped = 0
        self.no_words = self.mysql_connection.get_no_words()

    async def add_black_list(self, ctx, id):
        self.mysql_connection.update_blacklist(
            id, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        )
        await ctx.reply("user added to blacklist")

    async def remove_black_list(self, ctx, id):
        if self.mysql_connection.is_exist("user_id", id, "users", "blacklist"):
            await ctx.reply("user not found")
            return False

        self.mysql_connection.update_blacklist(id, None)
        await ctx.reply("user removed from blacklist")
        return True

    async def add_no_words(self, ctx, words):
        for word in words:
            if self.check(word, self.no_words):
                return await ctx.reply("word/words already exist")

            self.mysql_connection.add_noWords(word.lower())
        await ctx.reply("word/words added")
        self.no_words = self.mysql_connection.get_no_words()

    async def remove_no_words(self, ctx, words):
        for word in words:
            if not self.check(word, self.no_words):
                return await ctx.reply("word/words doesn't exist")

            self.mysql_connection.remove_noWords(word.lower())
        await ctx.reply("word/words removed")
        self.no_words = self.mysql_connection.get_no_words()

    def check(self, id, lst):
        if id in lst:
            return True
        return False

    def check_black_list(self, id):
        date = self.mysql_connection.get_user_data(id, "blacklist")
        if date:
            diff = datetime.datetime.now() - date

            if diff.total_seconds() / 60 > 180:
                with open(self.blacklist_db, "w") as bl:
                    self.mysql_connection.update_blacklist(id, None)
                return False
            return True

        return False

    @DeprecationWarning
    def count_black_list(self, id):
        if not id in self.no_spam:
            self.no_spam[id] = [0, datetime.datetime.now()]

        diff = datetime.datetime.now() - self.no_spam[id][1]
        if diff.total_seconds() / 60 > 10:
            self.no_spam[id] = [1, datetime.datetime.now()]
        else:
            self.no_spam[id][0] += 1
            self.no_spam[id][1] = datetime.datetime.now()

        if self.no_spam[id][0] >= 5:
            black_list = json.load(open(self.blacklist_db))
            with open(self.blacklist_db, "w") as bl:
                black_list[id] = datetime.datetime.now().strftime(
                    "%d-%b-%Y (%H:%M:%S.%f)"
                )
                json.dump(black_list, bl)
                del self.no_spam[id]

    @DeprecationWarning
    def checkWarns(self, id):
        if id in self.no_spam:
            diff = datetime.datetime.now() - self.no_spam[id][1]
            if diff.total_seconds() / 60 > 10:
                return 0
            return self.no_spam[id][0]

        return 0

    def censured(self, msg):
        msg = msg.lower()
        for word in self.no_words:
            msg = msg.replace(word, "*")
        return msg
