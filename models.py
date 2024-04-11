import sqlite3


def init_db():
    connection = sqlite3.connect('data.db', check_same_thread=False)
    cursor = connection.cursor()
    
    cursor.execute("""DROP TABLE IF EXISTS users""") 
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    name TEXT NOT NULL,
    password TEXT NOT NULL
    );""")
    cursor.execute("""INSERT OR IGNORE INTO users VALUES (NULL,'admin@gmail.com', 'admin', 'admin')""")
    cursor.execute("""INSERT OR IGNORE INTO users VALUES (NULL,'user1@gmail.com', 'User1', '1' )""")
    cursor.execute("""INSERT OR IGNORE INTO users VALUES (NULL,'user2@gmail.com', 'User2', '2' )""")
    