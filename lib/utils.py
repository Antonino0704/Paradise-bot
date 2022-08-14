import json


database = 'database.json'

class Utils:
    def __init__(self):
        pass
    
    def get_prefix(self, bot, msg):
        data = json.load(open(database))
        return data[msg.guild.name]["prefix"]