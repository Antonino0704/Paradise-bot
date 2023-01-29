import mysql.connector


class Mysql:
    def __init__(self, address, usr, passwd):
        self.db = mysql.connector.connect(
            host = address,
            user = usr,
            password = passwd,
            database = "paradise_database",
            autocommit = True
        )

        self.cursor = self.db.cursor()

    def guild_join(self, guild_id, guild_name):
        query = """
                INSERT INTO guilds(guild_id, name)
                VALUES (%s, %s)
                """
        data = (str(guild_id), guild_name)
        self.cursor.execute(query, data)
        self.db.commit()

    def get_emoji_icon(self, emoji_id):
        query = """
                SELECT icon
                FROM items
                WHERE item_id = %s
                """
        data = (emoji_id, )
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        return result[0][0]
    
    def get_all_emoji_icon(self):
        query = """
                SELECT icon
                FROM items
                ORDER BY item_id
                """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    def get_badge_icon(self, emoji_id):
        query = """
                SELECT icon
                FROM badges
                WHERE badge_id = %s
                """
        data = (emoji_id, )
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        return result[0][0]
    
    def get_badge_icon_all(self, user_id):
        query = """
                SELECT icon
                FROM badges
                    INNER JOIN inventories
                    ON badges.badge_id = inventories.badge_id
                WHERE user_id = %s
                """
        data = (user_id, )
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        return " " if len(result) == 0 else result

    def get_guild_data(self, guild_id, attribute):
        query = f"""
                SELECT {attribute}
                FROM guilds
                WHERE guild_id = %s
                """
        data = (guild_id, )
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        return result[0][0]
    
    def get_guild_data_managerVC(self, guild_id, attributes):
        query = f"""
                SELECT {attributes}
                FROM guilds
                WHERE guild_id = %s
                """
        data = (str(guild_id), )
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        return False if len(result) == 0 else result
    
    def get_user_data(self, user_id, attribute):
        query = f"""
                SELECT {attribute}
                FROM users
                WHERE user_id = %s
                """
        data = (user_id, )
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        return False if len(result) == 0 else result[0][0]
    
    def get_user_names(self, user_id, attribute):
        query = f"""
                SELECT {attribute}
                FROM users
                WHERE user_id = %s
                """
        data = (user_id, )
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        return False if len(result) == 0 else result
    
    def get_user_job(self, user_id):
        query = f"""
                SELECT name
                FROM users
                    INNER JOIN jobs
                    ON users.work_id = jobs.work_id
                WHERE user_id = %s
                """
        data = (user_id, )
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        return None if len(result) == 0 else result[0][0]
    
    def get_no_words(self):
        query = """
                SELECT word
                FROM noWords
                """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return [i[0] for i in result]
    
    def get_work_by_name(self, work_name):
        query = """
                SELECT work_id
                FROM jobs
                WHERE name = %s
                """
        data = (work_name, )
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        return False if len(result) == 0 else result[0][0]
    
    def get_badge_by_icon(self, icon):
        query = """
                SELECT badge_id
                FROM badges
                WHERE icon = %s
                """
        data = (icon, )
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        return False if len(result) == 0 else result[0][0]
    
    def get_pokedex(self, user_id, item_id):
        query = """
                SELECT amount
                FROM pokedex
                WHERE user_id = %s and item_id = %s
                """
        data = (user_id, item_id)
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        return False if len(result) == 0 else result[0][0]
    
    def get_pokedex_all(self, user_id):
        query = """
                SELECT items.icon, pokedex.amount
                FROM pokedex
	                INNER JOIN items
	                ON pokedex.item_id = items.item_id
                WHERE user_id = %s
                """
        data = (user_id, )
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        return result
    
    def get_robux_list(self):
        query = """
                SELECT user_id, amount
                FROM pokedex
                WHERE item_id = 1
                ORDER BY amount DESC
                """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return False if len(result) == 0 else result
    
    def get_role_id_price(self, guild_id):
        query = f"""
                SELECT role_id, price
                FROM roles
                WHERE guild_id = %s
                """
        data = (guild_id, )
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        return False if len(result) == 0 else result
    
    def get_role_price(self, role_id):
        query = f"""
                SELECT price
                FROM roles
                WHERE role_id = %s
                """
        data = (role_id, )
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        return False if len(result) == 0 else result[0][0]
    
    def get_info(self, pk, table_id, table):
        query = f"""
                SELECT name, description
                FROM {table}
                WHERE {pk} = %s
                """
        data = (table_id, )
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        return result
    
    def get_badge_date(self, user_id, badge_name):
        query = f"""
                SELECT received
                FROM inventories
                    INNER JOIN badges
                    ON inventories.badge_id = badges.badge_id
                WHERE user_id = %s AND badges.name = %s
                """
        data = (user_id, badge_name)
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        return " " if len(result) == 0 else result[0][0]

    def is_exist(self, pk, table_id, table, attribute):
        query = f"""
                SELECT ISNULL({attribute})
                FROM {table}
                WHERE {pk} = %s
                """
        data = (str(table_id), )
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        return True if len(result) == 0 else result[0][0]
    
    def is_exist_composite(self, pk1, pk2, table_id1, table_id2, table, attribute):
        query = f"""
                SELECT ISNULL({attribute})
                FROM {table}
                WHERE {pk1} = %s and {pk2} = %s
                """
        data = (str(table_id1),table_id2)
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        return True if len(result) == 0 else result[0][0]
    
    def add_noWords(self, word):
        query = f"""
                INSERT INTO noWords(word)
                VALUES (%s)
                """
        data = (word, )
        self.cursor.execute(query, data)
        self.db.commit()

    def remove_noWords(self, word):
        query = f"""
                DELETE FROM noWords
                WHERE word = %s
                """
        data = (word, )
        self.cursor.execute(query, data)
        self.db.commit()

    def add_badge(self, name, description, icon):
        query = """
                INSERT INTO badges(name, description, icon)
                VALUES (%s, %s, %s)
                """
        data = (name, description, icon)
        self.cursor.execute(query, data)
        self.db.commit()

    def remove_badges(self, badge_id):
        query = f"""
                DELETE FROM badges
                WHERE badge_id = %s
                """
        data = (badge_id, )
        self.cursor.execute(query, data)
        self.db.commit()

    def add_badge_to_user(self, user_id, badge_id):
        query = """
                INSERT INTO inventories(user_id, badge_id, received)
                VALUES (%s, %s, NOW())
                """
        data = (str(user_id), badge_id)
        self.cursor.execute(query, data)
        self.db.commit()

    def delete_badge_to_user(self, user_id, badge_id):
        query = f"""
                DELETE FROM inventories
                WHERE user_id = %s and badge_id = %s
                """
        data = (user_id, badge_id)
        self.cursor.execute(query, data)
        self.db.commit()

    def add_role(self, role_id, name, price, guild_id):
        query = """
                INSERT INTO roles(role_id, name, price, guild_id)
                VALUES (%s, %s, %s, %s)
                """
        data = (str(role_id), name, price, str(guild_id))
        self.cursor.execute(query, data)
        self.db.commit()

    def delete_role(self, role_id):
        query = f"""
                DELETE FROM roles
                WHERE role_id = %s
                """
        data = (role_id, )
        self.cursor.execute(query, data)
        self.db.commit()

    def update_blacklist(self, user_id, time):
        query = """
                UPDATE users
                SET blacklist = %s
                WHERE user_id = %s
                """
        data = (time, user_id)
        self.cursor.execute(query, data)
        self.db.commit()

    def update_work(self, user_id, work_id):
        query = f"""
                UPDATE users
                SET work_id = %s
                WHERE user_id = %s
                """
        data = (work_id, user_id)
        self.cursor.execute(query, data)
        self.db.commit()

    def update_pokedex(self, user_id, item_id, amount):
        query = """
                UPDATE pokedex
                SET amount = %s
                WHERE user_id = %s and item_id = %s
                """
        data = (amount, user_id, item_id)
        self.cursor.execute(query, data)
        self.db.commit()

    def update_guild_data(self, guild_id, attribute, value):
        query = f"""
                UPDATE guilds
                SET {attribute} = %s
                WHERE guild_id = %s
                """
        data = (value, guild_id)
        self.cursor.execute(query, data)
        self.db.commit()

    def update_user_names(self, user_id, firstname, lastname):
        query = f"""
                UPDATE users
                SET firstname = %s, lastname = %s
                WHERE user_id = %s
                """
        data = (firstname, lastname, user_id)
        self.cursor.execute(query, data)
        self.db.commit()

    def add_user(self, user_id):
        query = """
                INSERT INTO users(user_id)
                VALUES (%s)
                """
        data = (str(user_id), )
        self.cursor.execute(query, data)
        self.db.commit()

    def add_item_to_user(self, user_id, item_id):
        query = """
                INSERT INTO pokedex(user_id, item_id)
                VALUES (%s, %s)
                """
        data = (str(user_id), item_id)
        self.cursor.execute(query, data)
        self.db.commit()