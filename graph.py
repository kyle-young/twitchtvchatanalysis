#!/usr/bin/env python3

# Helpful links
# http://stackoverflow.com/questions/16496017/typeerror-when-using-matplotlibs-strpdate2num-with-python-3-2
# http://stackoverflow.com/questions/1822928/sqlite-group-by

import sqlite3
import time
import datetime

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# gets the name of the db in the "settings" file 
with open('settings','r') as s:
    # need to use strip to get rid of newline that python adds when it reads a file
    game_db = s.readline().strip()

db = sqlite3.connect(game_db)

#-------------------------------------------------------------------------------------------------

# get number of messages per minute from sqlite
sql = "SELECT strftime('%Y-%m-%dT%H:%M:00', datetime), count() FROM logs GROUP BY strftime('%Y-%m-%dT%H:%M:00', datetime)"

# get game start time
sql_gamestart = "SELECT strftime('%Y-%m-%dT%H:%M:00', datetime) FROM logs GROUP BY  strftime('%Y-%m-%dT%H:%M:00', datetime) LIMIT 1"

GAMESTART = db.execute(sql_gamestart).fetchone()[0]

graph_array = []

def bytedate2num(fmt):
    def converter(b):
        return mdates.strpdate2num(fmt)(b.decode('ascii'))
    return converter

def todatetime(datetime_str):
    return datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:00')



for row in db.execute(sql):
    data = str(row).replace(')','').replace('(','').replace('u\'','').replace("'", "")
    
    # Replace uncommented code with commented code to graph using real time instead of game time

    #split_data = data.split(',')
    #split_data[0] = str(todatetime(split_data[0])-todatetime(GAMESTART))
    #new_data = ','.join(split_data)
    #graph_array.append(new_data)
    #print(new_data)

    graph_array.append(data)
    print(data)


#datetime, value = np.loadtxt(graph_array, delimiter=',', unpack=True, converters={0: bytedate2num("%H:%M:%S")})
datetime, value = np.loadtxt(graph_array, delimiter=',', unpack=True, converters={0: bytedate2num("%Y-%m-%dT%H:%M:00")})

plt.xlabel("Time elapsed")
plt.ylabel("Number of messages per minute")
plt.plot_date(x=datetime, y=value,fmt = "b")
plt.show()

db.close()
