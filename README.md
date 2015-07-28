# twitchtvchatanalysis
Ingests twitch.tv irc chat, stores it in SQLite, graphs using matplotlib.

To use (after you get all the require credentials):
1. Put the SQLite database name you want in the settings file  
2. Run createdb.py by typing in "python3 createdb.py"  
3. When you want go get twitch.tv chat type in "python3 twitchingest.py"  
4. To graph, type in "python3 graph.py"  
