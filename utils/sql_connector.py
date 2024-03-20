import sqlite3
from datetime import datetime, timedelta
from config import KILLS_TO_LEVEL_UP


class SQliteConnector:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.connection.commit()
        self.cursor = self.connection.cursor()

        # race table
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Races (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                base_health INTEGER,
                base_damage INTEGER
                );
                ''')

        # users table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        health INTEGER NOT NULL,
        damage INTEGER NOT NULL,
        max_health INTEGER NOT NULL,
        level INTEGER NOT NULL,
        level_points INTEGER NOT NULL,
        kills INTEGER NOT NULL,
        rid INTEGER NOT NULL,
        dead_until TEXT,
        FOREIGN KEY (rid) REFERENCES Races (id)
        );
        ''')

        self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Admins (
                        id INTEGER PRIMARY KEY);
                        ''')

        # await self.add_user(1121111, 'huilo', 2)

    async def add_user(self, uid: int, name: str, rid: int):
        self.cursor.execute(f'''
    INSERT INTO Users (id, name, health, damage, max_health, level, level_points, kills, rid, dead_until)
    SELECT 
    {uid}, 
    '{name}', 
    (SELECT base_health FROM Races WHERE id = {rid}),
    (SELECT base_damage FROM Races WHERE id = {rid}),
    (SELECT base_health FROM Races WHERE id = {rid}),
    1,
    0,
    0,
    {rid},
    '{datetime.now()}'
    WHERE NOT EXISTS(SELECT * FROM Users WHERE id = {uid});
    ''')
        self.connection.commit()

    async def add_damage(self, uid: int, amount: int):
        self.cursor.execute(f'''
                        UPDATE Users
                        SET damage = damage + {amount}
                        WHERE id = {uid};
                        ''')

        self.connection.commit()

    async def level_up(self, uid: int):
        self.cursor.execute(f'''
                        UPDATE Users
                        SET level = level + 1
                        WHERE id = {uid};
                        ''')

        self.connection.commit()

    async def add_max_health(self, uid: int, amount: int):
        self.cursor.execute(f'''
                        UPDATE Users
                        SET max_health = max_health + {amount}
                        WHERE id = {uid};
                        ''')
        self.cursor.execute(f'''
                                UPDATE Users
                                SET health = max_health
                                WHERE id = {uid};
                                ''')
        self.connection.commit()

    async def reduce_level_points(self, uid: int):
        self.cursor.execute(f'''
                                UPDATE Users
                                SET level_points = level_points - 1
                                WHERE id = {uid};
                                ''')

        self.connection.commit()

    async def add_level_point(self, uid: int):

        self.cursor.execute(f'''
                                        UPDATE Users
                                        SET level_points = level_points + 1
                                        WHERE id = {uid};
                                        ''')

        self.connection.commit()

    async def attack(self, uaid: int, udid: int):
        _lvl_up = False
        self.cursor.execute(f'''
                UPDATE Users
                SET health = health - (SELECT damage FROM Users WHERE id = {uaid})
                WHERE id = {udid};
                ''')

        if await self.get_health(udid) <= 0:

            self.cursor.execute(f'''UPDATE Users 
                SET 
                kills = kills + 1
                WHERE id = {uaid};''')
            if await self.get_kills(uaid) in KILLS_TO_LEVEL_UP:
                await self.add_level_point(uaid)
                await self.level_up(uaid)
                _lvl_up = True

        self.cursor.execute(f'''
        UPDATE Users SET
                        dead_until = '{datetime.now() + timedelta(seconds=60)}',
                        health = Users.max_health
                        WHERE health <= 0 AND id = {udid};
        ''')
        self.connection.commit()
        return _lvl_up

    async def get_user(self, uid: int):
        return self.cursor.execute(f'''
                SELECT * FROM Users WHERE id = {uid};
                ''').fetchone()

    async def get_kills(self, uid: int):
        return int(self.cursor.execute(f'''
                        SELECT kills FROM Users WHERE id = {uid};
                        ''').fetchone()['kills'])

    async def get_level_points(self, uid: int):
        return self.cursor.execute(f'''
                        SELECT level_points FROM Users WHERE id = {uid};
                        ''').fetchone()['level_points']

    async def get_users_id(self):
        return self.cursor.execute(f'''SELECT id FROM Users;''').fetchall()

    async def get_health(self, uid: int):
        return self.cursor.execute(f'''
                        SELECT health FROM Users WHERE id = {uid};
                        ''').fetchone()['health']

    async def user_is_dead(self, uid: int):
        d = datetime.fromisoformat(self.cursor.execute(f'''
                        SELECT dead_until FROM Users WHERE id = {uid};
                        ''').fetchone()['dead_until'])

        return None if d < datetime.now() else d

    async def is_admin(self, uid: int):
        return len(self.cursor.execute(f'''
                        SELECT * FROM Admins WHERE id = {uid};
                        ''').fetchall()) > 0

    async def clear_users(self):
        self.cursor.execute(f'''DELETE FROM Users;''')
        self.connection.commit()

    async def get_race_name(self, rid: int):
        return self.cursor.execute(f'''
                        SELECT * FROM Races WHERE id = {rid};
                        ''').fetchone()['name']
    # def add_race(self, name: str, base_health: int, base_damage: int):
    #  self.cursor.execute(f'''
    #            INSERT INTO Races (name, base_health, base_damage)
    #            VALUES ('{name}', {base_health}, {base_damage});''')
    #    self.connection.commit()

# f = SQliteConnector('db.db')
