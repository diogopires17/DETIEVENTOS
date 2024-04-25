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

    cursor.execute("""DROP TABLE IF EXISTS events""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    description TEXT NOT NULL,
    location TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
    );""")
    cursor.execute("""INSERT OR IGNORE INTO events VALUES (NULL, 'Workshop Android', '16-09-2024', 'Android Workshop', 'DETI', 1)""")
   # cursor.execute("""INSERT OR IGNORE INTO events VALUES (NULL, 'Workshop Python', '16-09-2024', 'Python Workshop', 'DETI', 1)""")
    #cursor.execute("""INSERT OR IGNORE INTO events VALUES (NULL, 'Workshop Java', '16-09-2024', 'Java Workshop', 'DETI', 1)""")
    #cursor.execute("""INSERT OR IGNORE INTO events VALUES (NULL, 'Workshop C', '16-09-2024', 'C Workshop', 'DETI', 1)""")
    #cursor.execute("""INSERT OR IGNORE INTO events VALUES (NULL, 'Workshop C++', '16-09-2024', 'C++ Workshop', 'DETI', 1)""")
    #cursor.execute("""INSERT OR IGNORE INTO events VALUES (NULL, 'Workshop Ruby', '16-09-2024', 'Ruby Workshop', 'DETI', 1)""")
    #cursor.execute("""INSERT OR IGNORE INTO events VALUES (NULL, 'Workshop PHP', '16-09-2024', 'PHP Workshop', 'DETI', 1)""")
    connection.commit()

#                               FUNÇÕES AUXILIARES

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