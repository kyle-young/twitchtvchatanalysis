# twitchtvchatanalysis
Ingests twitch.tv irc chat, stores it in SQLite, graphs using matplotlib.

To use (after you get all the require credentials):  
  
1. Put the SQLite database name you want in the settings file  
2. Run createdb.py by typing in "python3 createdb.py"  
3. Get all of the IRC connection info

    -For oauth key: www.twitchapps.com/tmi/

    -For IRC connection info: https://api.twitch.tv/api/channels/<channel_name>/chat_properties
4. When you want go get twitch.tv chat type in "python3 twitchingest.py"  
5. To graph, type in "python3 graph.py"  
