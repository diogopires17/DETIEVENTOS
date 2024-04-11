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