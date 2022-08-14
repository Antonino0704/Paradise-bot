import json
import datetime

class Spam:
    def __init__(self):
        self.no_spam = {}
        self.msg_stopped = 0
        self.no_words = json.load(open("no_words.json"))["no_words"]
        
    def check_black_list(self, id):
        black_list = json.load(open("blacklist.json"))
        if id in black_list:
            diff = datetime.datetime.now() - datetime.datetime.strptime(black_list[id], "%d-%b-%Y (%H:%M:%S.%f)")
            
            if diff.total_seconds() / 60 > 180:
                with open("blacklist.json", 'w') as bl:
                    del black_list[id]
                    json.dump(black_list, bl)
                return False
            return True
        
        return False
    
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
            black_list = json.load(open("blacklist.json"))
            with open("blacklist.json", 'w') as bl:
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
    
    def censured(self, id, msg):
        if id != 533014724569333770:
            for word in self.no_words:
                msg = msg.replace(word, "*")
        return msg