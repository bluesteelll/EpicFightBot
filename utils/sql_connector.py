import sqlite3


class SQliteConnector:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.connection.commit()
        self.cursor = self.connection.cursor()

        #race table
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Races (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                base_health INTEGER,
                base_damage INTEGER
                );
                ''')

        #users table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        health INTEGER,
        damage INTEGER,
        rid INTEGER,
        is_alive INTEGER NOT NULL,
        FOREIGN KEY (rid) REFERENCES Races (id)
        );
        ''')

        #await self.add_user(1121111, 'huilo', 2)

    async def add_user(self, uid: int, name: str, rid:int):
        self.cursor.execute(f'''
    INSERT INTO Users (id, name, health, damage, rid, is_alive)
    SELECT {uid}, 
    '{name}', 
    (SELECT base_health FROM Races WHERE id = {rid}),
    (SELECT base_damage FROM Races WHERE id = {rid}),
    {rid}, 
    1
    WHERE NOT EXISTS(SELECT * FROM Users WHERE id = {uid});
    ''')
        self.connection.commit()



    #def add_race(self, name: str, base_health: int, base_damage: int):
    #  self.cursor.execute(f'''
    #            INSERT INTO Races (name, base_health, base_damage)
    #            VALUES ('{name}', {base_health}, {base_damage});''')
    #    self.connection.commit()

#f = SQliteConnector('db.db')
