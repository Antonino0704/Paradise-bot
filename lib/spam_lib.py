import json
import datetime

class Spam:
    def __init__(self):
        self.data_files()
        self.no_spam = {}
        #self.msg_stopped = 0
        self.no_words = json.load(open(self.no_words_db))["no_words"]
        
    def data_files(self):
        self.no_words_db = 'jsonFile/no_words.json'
        self.blacklist_db = 'jsonFile/blacklist.json'
        
    async def add_black_list(self, ctx, id):
         black_list = json.load(open(self.blacklist_db))
         with open(self.blacklist_db, 'w') as bl:
             black_list[id] = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
             json.dump(black_list, bl)
             await ctx.reply("user added to blacklist")
             
    async def remove_black_list(self, ctx, id):
        black_list = json.load(open(self.blacklist_db))
        if self.check(id, black_list):
            with open(self.blacklist_db, 'w') as bl:
                del black_list[id]
                json.dump(black_list, bl)
                await ctx.reply("user removed from blacklist")
        else:
            await ctx.reply("user not found")
            return
        
    async def add_no_words(self, ctx, words):
        no_words = json.load(open(self.no_words_db))
        with open(self.no_words_db, 'w') as nw:
            for word in words:
                no_words["no_words"].append(word.lower())
                
            json.dump(no_words, nw)
            await ctx.reply("word/words added")
        self.no_words = json.load(open(self.no_words_db))["no_words"]
        
    async def remove_no_words(self, ctx, words):
        no_words = json.load(open(self.no_words_db))
        with open(self.no_words_db, 'w') as nw:
            for word in words:
                if self.check(word, no_words["no_words"]):
                    no_words["no_words"].remove(word.lower())
                    
            json.dump(no_words, nw)
            await ctx.reply("word/words removed")
        self.no_words = json.load(open(self.no_words_db))["no_words"]
        
    def check(self, id, lst):
        if id in lst:
            return True
        return False
        
    def check_black_list(self, id):
        black_list = json.load(open(self.blacklist_db))
        if id in black_list:
            diff = datetime.datetime.now() - datetime.datetime.strptime(black_list[id], "%d-%b-%Y (%H:%M:%S.%f)")
            
            if diff.total_seconds() / 60 > 180:
                with open(self.blacklist_db, 'w') as bl:
                    del black_list[id]
                    json.dump(black_list, bl)
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
            with open(self.blacklist_db, 'w') as bl:
                black_list[id] = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
                json.dump(black_list, bl)
                del self.no_spam[id]
                
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