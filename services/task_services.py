import sqlite3

DB_name="database.db"

def get_connection():
    return sqlite3.connect(DB_name)

def create_table():
    conn=get_connection()
    curor=conn.cursor()
    
    curor.execute("""CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                      title TEXT NOT NULL,
                                                      completed INTEGER DEFAULT 0 )""")
    
    conn.commit()
    conn.close()
    
    
    
    
    