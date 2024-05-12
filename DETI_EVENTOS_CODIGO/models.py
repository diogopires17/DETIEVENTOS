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
    cursor.execute("""INSERT OR IGNORE INTO users VALUES (NULL,'user1@gmail.com', 'António', '1' )""")
    cursor.execute("""INSERT OR IGNORE INTO users VALUES (NULL,'user2@gmail.com', 'User2', '2' )""")

    cursor.execute("""DROP TABLE IF EXISTS events""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    location TEXT NOT NULL,
    image TEXT,
    date DATE,
    user_id INTEGER,           
    colaborator TEXT , 
    vagas INTEGER,
    lotacao INTEGER,
    preco INTEGER,
    esgotado boolean DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(id)
    );""")

    cursor.execute("""INSERT OR IGNORE INTO events VALUES (NULL, 'Workshop Android', 'Android Workshop', 'DETI', 'static/img/android.png', '2024-06-27',1, 'NEECT', 15, 20, 0, 0)""")    
    cursor.execute("""INSERT OR IGNORE INTO events VALUES (NULL, 'Workshop Python', 'Python Workshop', 'DETI', 'static/img/python.png', '2024-07-06', 2, 'NEECT', 10, 15, 10, 0 )""")    
    cursor.execute("""INSERT OR IGNORE INTO events VALUES (NULL, 'Palestra Dart', 'Palestra', 'Maker Lab', 'static/img/dart.svg', '2022-05-07', 2, 'NEI', 30,30, 3, 1)""")   
    cursor.execute("""INSERT OR IGNORE INTO events VALUES (NULL, 'Feira de empresas', 'Feira de empresas', 'Aquário', 'static/img/feira.jpg', '2024-05-15', 1, 'NEET', 10, 12, 5, 0 )""")    
    
    cursor.execute("""DROP TABLE IF EXISTS user_events""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_events (
    user_id INTEGER,
    event_id INTEGER,
    PRIMARY KEY(user_id, event_id),
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(event_id) REFERENCES events(id)
    );""")
    cursor.execute("""INSERT OR IGNORE INTO user_events VALUES (2, 1)""")
    cursor.execute("""INSERT OR IGNORE INTO user_events VALUES (2, 4)""")




   
    
    #cursor.execute("""INSERT OR IGNORE INTO events VALUES (NULL, 'Workshop C', '16-09-2024', 'C Workshop', 'DETI', 1)""")
    #cursor.execute("""INSERT OR IGNORE INTO events VALUES (NULL, 'Workshop C++', '16-09-2024', 'C++ Workshop', 'DETI', 1)""")
    #cursor.execute("""INSERT OR IGNORE INTO events VALUES (NULL, 'Workshop Ruby', '16-09-2024', 'Ruby Workshop', 'DETI', 1)""")
    #cursor.execute("""INSERT OR IGNORE INTO events VALUES (NULL, 'Workshop PHP', '16-09-2024', 'PHP Workshop', 'DETI', 1)""")
    connection.commit()

#                               FUNÇÕES AUXILIARES
def get_user_id(email):
    connection = sqlite3.connect('data.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    user_id = cursor.fetchall()
    if len(user_id) == 0:
        return None
    return user_id[0][0]
def authenticate_user(email, password):
    if '/' in email:
        return False, "email can't contain character '/'"
    connection = sqlite3.connect('data.db', check_same_thread=False)
    cursor = connection.cursor()
    
    try:
        cursor.execute( "SELECT email, password, name FROM users WHERE email= ? AND password = ?", (email, password))
        results = cursor.fetchall()
        if len(results) == 0:
            return False, "Incorrect email or password", None, None, None
        
        return True, "", results[0][0], results[0][1], results[0][2]
    
    except Exception as e:
        print(e)
        return False, "There was an error validating your input, please check your data and try again.", None, None, None
    
def get_events():
    connection = sqlite3.connect('data.db', check_same_thread=False)
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT * FROM events")
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(e)
        return None
    
def get_user_events(user_id):
    connection = sqlite3.connect('data.db', check_same_thread=False)
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT * FROM user_events WHERE user_id = ?", (user_id,))
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(e)
        return None
    
def get_user_associated_events(user_id):
    connection = sqlite3.connect('data.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""
    SELECT events.* 
    FROM events 
    JOIN user_events ON events.id = user_events.event_id 
    WHERE user_events.user_id = ?
    """, (user_id,))
    return cursor.fetchall()