#!/usr/bin/env python3

import sqlite3

# gets the name of the db in the "settings" file
with open('settings','r') as s:
    # need to use strip to get rid of newline that python adds when it reads a file
    game_db = s.readline().strip()

conn = sqlite3.connect(game_db)
print("Opened db successfully")
c = conn.cursor()

c.execute('''CREATE TABLE logs (datetime TEXT, message TEXT)''')
print("Table created successfully")

conn.commit()
conn.close()
