import sqlite3
from flask import Flask

app = Flask(__name__)
DATABASE= 'mybase.db'





def init_db():
    db = sqlite3.connect('mybase.db')
    cursor = db.cursor()
    Sql_create_query = '''CREATE TABLE IF NOT EXISTS user(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            lastname TEXT NOT NULL,
                            age INTEGER NOT NULL,
                            email TEXT NOT NULL,
                            description TEXT);'''


    print("succesfully connected to db")
    cursor.execute(Sql_create_query)
    db.commit()
    print("user table created")


    db.close()





def create_table():
    db = sqlite3.connect('mybase.db')
    cursor=db.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS admins(
                    userID INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(20) NOT NULL,
                    firstname VARCHAR(20) NOT NULL,
                    lastname VARCHAR(20) NOT NULL,
                    password VARCHAR(20) NOT NULL);
                                                ''')
    db.close()

def data_entry():
    db = sqlite3.connect('mybase.db')
    cursor = db.cursor()
    cursor.execute("""
    INSERT INTO admins (username, firstname, lastname, password)
    VALUES ('admin', 'admin', 'admin', 'admin')
    """)
    db.commit()
    db.close()


if __name__=='__main__':
    init_db()
    create_table()
    data_entry()
