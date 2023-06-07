import mysql.connector


class Mysql:
    def __init__(self, address, usr, passwd):
        self.address = address
        self.usr = usr
        self.passwd = passwd

    def connection(self):
        return mysql.connector.connect(
            host=self.address,
            user=self.usr,
            password=self.passwd,
            database="paradise_database",
            autocommit=True,
        )

    def close(self, db, cursor):
        cursor.close()
        db.close()

    def guild_join(self, guild_id, guild_name):
        db = self.connection()
        cursor = db.cursor()
        query = """
                INSERT INTO guilds(guild_id, name)
                VALUES (%s, %s)
                """
        data = (str(guild_id), guild_name)
        cursor.execute(query, data)
        db.commit()
        self.close(db, cursor)

    def get_emoji_icon(self, emoji_id):
        db = self.connection()
        cursor = db.cursor()
        query = """
                SELECT icon
                FROM items
                WHERE item_id = %s
                """
        data = (emoji_id,)
        cursor.execute(query, data)
        result = cursor.fetchall()
        self.close(db, cursor)
        return result[0][0]

    def get_all_emoji_icon(self):
        db = self.connection()
        cursor = db.cursor()
        query = """
                SELECT icon
                FROM items
                ORDER BY item_id
                """
        cursor.execute(query)
        result = cursor.fetchall()
        self.close(db, cursor)
        return result

    def get_badge_icon(self, emoji_id):
        db = self.connection()
        cursor = db.cursor()
        query = """
                SELECT icon
                FROM badges
                WHERE badge_id = %s
                """
        data = (emoji_id,)
        cursor.execute(query, data)
        result = cursor.fetchall()
        self.close(db, cursor)
        return result[0][0]

    def get_badge_icon_all(self, user_id):
        db = self.connection()
        cursor = db.cursor()
        query = """
                SELECT icon
                FROM badges
                    INNER JOIN inventories
                    ON badges.badge_id = inventories.badge_id
                WHERE user_id = %s
                """
        data = (user_id,)
        cursor.execute(query, data)
        result = cursor.fetchall()
        self.close(db, cursor)
        return " " if len(result) == 0 else result

    def get_guild_data(self, guild_id, attribute):
        db = self.connection()
        cursor = db.cursor()
        query = f"""
                SELECT {attribute}
                FROM guilds
                WHERE guild_id = %s
                """
        data = (guild_id,)
        cursor.execute(query, data)
        result = cursor.fetchall()
        self.close(db, cursor)
        return result[0][0]

    def get_guild_data_managerVC(self, guild_id, attributes):
        db = self.connection()
        cursor = db.cursor()
        query = f"""
                SELECT {attributes}
                FROM guilds
                WHERE guild_id = %s
                """
        data = (str(guild_id),)
        cursor.execute(query, data)
        result = cursor.fetchall()
        self.close(db, cursor)
        return False if len(result) == 0 else result

    def get_user_data(self, user_id, attribute):
        db = self.connection()
        cursor = db.cursor()
        query = f"""
                SELECT {attribute}
                FROM users
                WHERE user_id = %s
                """
        data = (user_id,)
        cursor.execute(query, data)
        result = cursor.fetchall()
        self.close(db, cursor)
        return False if len(result) == 0 else result[0][0]

    def get_user_names(self, user_id, attribute):
        db = self.connection()
        cursor = db.cursor()
        query = f"""
                SELECT {attribute}
                FROM users
                WHERE user_id = %s
                """
        data = (user_id,)
        cursor.execute(query, data)
        result = cursor.fetchall()
        self.close(db, cursor)
        return False if len(result) == 0 else result

    def get_user_job(self, user_id):
        db = self.connection()
        cursor = db.cursor()
        query = f"""
                SELECT name
                FROM users
                    INNER JOIN jobs
                    ON users.work_id = jobs.work_id
                WHERE user_id = %s
                """
        data = (user_id,)
        cursor.execute(query, data)
        result = cursor.fetchall()
        self.close(db, cursor)
        return None if len(result) == 0 else result[0][0]

    def get_no_words(self):
        db = self.connection()
        cursor = db.cursor()
        query = """
                SELECT word
                FROM noWords
                """
        cursor.execute(query)
        result = cursor.fetchall()
        self.close(db, cursor)
        return [i[0] for i in result]

    def get_work_by_name(self, work_name):
        db = self.connection()
        cursor = db.cursor()
        query = """
                SELECT work_id
                FROM jobs
                WHERE name = %s
                """
        data = (work_name,)
        cursor.execute(query, data)
        result = cursor.fetchall()
        self.close(db, cursor)
        return False if len(result) == 0 else result[0][0]

    def get_badge_by_icon(self, icon):
        db = self.connection()
        cursor = db.cursor()
        query = """
                SELECT badge_id
                FROM badges
                WHERE icon = %s
                """
        data = (icon,)
        cursor.execute(query, data)
        result = cursor.fetchall()
        self.close(db, cursor)
        return False if len(result) == 0 else result[0][0]

    def get_pokedex(self, user_id, item_id):
        db = self.connection()
        cursor = db.cursor()
        query = """
                SELECT amount
                FROM pokedex
                WHERE user_id = %s and item_id = %s
                """
        data = (user_id, item_id)
        cursor.execute(query, data)
        result = cursor.fetchall()
        self.close(db, cursor)
        return False if len(result) == 0 else result[0][0]

    def get_pokedex_all(self, user_id):
        db = self.connection()
        cursor = db.cursor()
        query = """
                SELECT items.icon, pokedex.amount
                FROM pokedex
	                INNER JOIN items
	                ON pokedex.item_id = items.item_id
                WHERE user_id = %s
                """
        data = (user_id,)
        cursor.execute(query, data)
        result = cursor.fetchall()
        self.close(db, cursor)
        return result

    def get_robux_list(self):
        db = self.connection()
        cursor = db.cursor()
        query = """
                SELECT user_id, amount
                FROM pokedex
                WHERE item_id = 1
                ORDER BY amount DESC
                """
        cursor.execute(query)
        result = cursor.fetchall()
        self.close(db, cursor)
        return False if len(result) == 0 else result

    def get_role_id_price(self, guild_id):
        db = self.connection()
        cursor = db.cursor()
        query = f"""
                SELECT role_id, price
                FROM roles
                WHERE guild_id = %s
                """
        data = (guild_id,)
        cursor.execute(query, data)
        result = cursor.fetchall()
        self.close(db, cursor)
        return False if len(result) == 0 else result

    def get_role_price(self, role_id):
        db = self.connection()
        cursor = db.cursor()
        query = f"""
                SELECT price
                FROM roles
                WHERE role_id = %s
                """
        data = (role_id,)
        cursor.execute(query, data)
        result = cursor.fetchall()
        self.close(db, cursor)
        return False if len(result) == 0 else result[0][0]

    def get_info(self, pk, table_id, table):
        db = self.connection()
        cursor = db.cursor()
        query = f"""
                SELECT name, description
                FROM {table}
                WHERE {pk} = %s
                """
        data = (table_id,)
        cursor.execute(query, data)
        result = cursor.fetchall()
        self.close(db, cursor)
        return result

    def get_badge_date(self, user_id, badge_name):
        db = self.connection()
        cursor = db.cursor()
        query = f"""
                SELECT received
                FROM inventories
                    INNER JOIN badges
                    ON inventories.badge_id = badges.badge_id
                WHERE user_id = %s AND badges.name = %s
                """
        data = (user_id, badge_name)
        cursor.execute(query, data)
        result = cursor.fetchall()
        self.close(db, cursor)
        return " " if len(result) == 0 else result[0][0]

    def is_exist(self, pk, table_id, table, attribute):
        db = self.connection()
        cursor = db.cursor()
        query = f"""
                SELECT ISNULL({attribute})
                FROM {table}
                WHERE {pk} = %s
                """
        data = (str(table_id),)
        cursor.execute(query, data)
        result = cursor.fetchall()
        self.close(db, cursor)
        return True if len(result) == 0 else result[0][0]

    def is_exist_composite(self, pk1, pk2, table_id1, table_id2, table, attribute):
        db = self.connection()
        cursor = db.cursor()
        query = f"""
                SELECT ISNULL({attribute})
                FROM {table}
                WHERE {pk1} = %s and {pk2} = %s
                """
        data = (str(table_id1), table_id2)
        cursor.execute(query, data)
        result = cursor.fetchall()
        self.close(db, cursor)
        return True if len(result) == 0 else result[0][0]

    def add_noWords(self, word):
        db = self.connection()
        cursor = db.cursor()
        query = f"""
                INSERT INTO noWords(word)
                VALUES (%s)
                """
        data = (word,)
        cursor.execute(query, data)
        db.commit()
        self.close(db, cursor)

    def remove_noWords(self, word):
        db = self.connection()
        cursor = db.cursor()
        query = f"""
                DELETE FROM noWords
                WHERE word = %s
                """
        data = (word,)
        cursor.execute(query, data)
        db.commit()
        self.close(db, cursor)

    def add_badge(self, name, description, icon):
        db = self.connection()
        cursor = db.cursor()
        query = """
                INSERT INTO badges(name, description, icon)
                VALUES (%s, %s, %s)
                """
        data = (name, description, icon)
        cursor.execute(query, data)
        db.commit()
        self.close(db, cursor)

    def remove_badges(self, badge_id):
        db = self.connection()
        cursor = db.cursor()
        query = f"""
                DELETE FROM badges
                WHERE badge_id = %s
                """
        data = (badge_id,)
        cursor.execute(query, data)
        db.commit()
        self.close(db, cursor)

    def add_badge_to_user(self, user_id, badge_id):
        db = self.connection()
        cursor = db.cursor()
        query = """
                INSERT INTO inventories(user_id, badge_id, received)
                VALUES (%s, %s, NOW())
                """
        data = (str(user_id), badge_id)
        cursor.execute(query, data)
        db.commit()
        self.close(db, cursor)

    def delete_badge_to_user(self, user_id, badge_id):
        db = self.connection()
        cursor = db.cursor()
        query = f"""
                DELETE FROM inventories
                WHERE user_id = %s and badge_id = %s
                """
        data = (user_id, badge_id)
        cursor.execute(query, data)
        db.commit()
        self.close(db, cursor)

    def add_role(self, role_id, name, price, guild_id):
        db = self.connection()
        cursor = db.cursor()
        query = """
                INSERT INTO roles(role_id, name, price, guild_id)
                VALUES (%s, %s, %s, %s)
                """
        data = (str(role_id), name, price, str(guild_id))
        cursor.execute(query, data)
        db.commit()
        self.close(db, cursor)

    def delete_role(self, role_id):
        db = self.connection()
        cursor = db.cursor()
        query = f"""
                DELETE FROM roles
                WHERE role_id = %s
                """
        data = (role_id,)
        cursor.execute(query, data)
        db.commit()
        self.close(db, cursor)

    def update_blacklist(self, user_id, time):
        db = self.connection()
        cursor = db.cursor()
        query = """
                UPDATE users
                SET blacklist = %s
                WHERE user_id = %s
                """
        data = (time, user_id)
        cursor.execute(query, data)
        db.commit()
        self.close(db, cursor)

    def update_work(self, user_id, work_id):
        db = self.connection()
        cursor = db.cursor()
        query = f"""
                UPDATE users
                SET work_id = %s
                WHERE user_id = %s
                """
        data = (work_id, user_id)
        cursor.execute(query, data)
        db.commit()
        self.close(db, cursor)

    def update_pokedex(self, user_id, item_id, amount):
        db = self.connection()
        cursor = db.cursor()
        query = """
                UPDATE pokedex
                SET amount = %s
                WHERE user_id = %s and item_id = %s
                """
        data = (amount, user_id, item_id)
        cursor.execute(query, data)
        db.commit()
        self.close(db, cursor)

    def update_guild_data(self, guild_id, attribute, value):
        db = self.connection()
        cursor = db.cursor()
        query = f"""
                UPDATE guilds
                SET {attribute} = %s
                WHERE guild_id = %s
                """
        data = (value, guild_id)
        cursor.execute(query, data)
        db.commit()
        self.close(db, cursor)

    def update_user_names(self, user_id, firstname, lastname):
        db = self.connection()
        cursor = db.cursor()
        query = f"""
                UPDATE users
                SET firstname = %s, lastname = %s
                WHERE user_id = %s
                """
        data = (firstname, lastname, user_id)
        cursor.execute(query, data)
        db.commit()
        self.close(db, cursor)

    def add_user(self, user_id):
        db = self.connection()
        cursor = db.cursor()
        query = """
                INSERT INTO users(user_id)
                VALUES (%s)
                """
        data = (str(user_id),)
        cursor.execute(query, data)
        db.commit()
        self.close(db, cursor)

    def add_item_to_user(self, user_id, item_id):
        db = self.connection()
        cursor = db.cursor()
        query = """
                INSERT INTO pokedex(user_id, item_id)
                VALUES (%s, %s)
                """
        data = (str(user_id), item_id)
        cursor.execute(query, data)
        db.commit()
        self.close(db, cursor)
