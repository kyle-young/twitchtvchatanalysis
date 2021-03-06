#!/usr/bin/env python3

import re
import socket
import datetime
import sqlite3

# Settings
HOST = ""            # Hostname of the IRC-Server, from https://api.twitch.tv/api/channels/{{channel_name}}/chat_properties
PORT = 443              # IRC-Port
CHAN = "#"        # Channelname = #{Nickname}, remember # sign
NICK = ""            # Nickname = Twitch username
PASS = "oauth:" # www.twitchapps.com/tmi/ will help to retrieve the required authkey

# gets the name of the db in the "settings" file  
with open('settings','r') as s:
    # need to use strip to get rid of newline that python adds when it reads a file
    game_db = s.readline().strip() 
# ---------------------------------------------------------------------------------------------

def send_pong(msg):
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(chan, msg):
    con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))


def send_nick(nick):
    con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password):
    con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(chan):
    con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(chan):
    con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))

def get_user(msg):
    msg = str(msg[0])
    user = msg[msg.find(":")+1:msg.find("!")]
    return user

def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result

# ---------------------------------------------------------------------------------------------

con = socket.socket()
con.connect((HOST, PORT))

send_pass(PASS)
send_nick(NICK)
join_channel(CHAN)

data = ""

db = sqlite3.connect(game_db)
db.execute('PRAGMA synchonous = OFF')
db.execute('PRAGMA journal_mode = MEMORY')

print("Opened db successfully")
db.execute('BEGIN;');
try:
    while True:
        try:
            data = con.recv(1024).decode('UTF-8', "ignore")
            data_split = re.split(r"[~\r\n]+", data)

            for line in data_split:
                line = str.split(line)
                time = datetime.datetime.now()
                if len(line) > 1:
                    if line[0] == 'PING':
                        send_pong("PONG")

                    if line[1] == 'PRIVMSG':
                        current_time = time.isoformat()
                        message = get_message(line)
                        user = get_user(line)
                        params = (current_time, user, message)

                        print(current_time + " : " + user +  " : " + message)
                        db.execute("INSERT INTO logs (datetime, user, message) VALUES (?,?,?)", params)

        except socket.error:
            print("Socket died")

        except socket.timeout:
            print("Socket timeout")
except KeyboardInterrupt:
    pass
        
db.commit()
print("committed!")
db.close()
