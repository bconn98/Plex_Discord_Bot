# Plex_Discord_Bot

This is a personal project developed by <a href=https://github.com/bconn98>Bryan Conn</a> and <a href=https://github.com/JarodGodlewski>Jarod Godlewski</a> to add flexabilty to a Plex Server
 using discord. 
 
### Install
```
git clone https://github.com/bconn98/Plex_Discord_Bot.git
pip3 install -r requirements.txt
```

### Run

It is required to own a .env file with the following variables:
- DISCORD_GUILD
    - The name of the discord server being linked to.
- DISCORD_TOKEN
    - Follow the directions defined <a href=https://www.writebots.com/discord-bot-token/>here</a>

- PLEX_URL
    - The remote access url for your plex server
- PLEX_TOKEN
    - Follow the directions defined <a href=https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/>here</a>
```
python3 bot.py
```

## Current Features
Please note that the command 'bog' exists as an inside joke to the developers and has no affect on plex servers. 
Additionally, pineapple is a reference to the TV show Psych.
```
​No Category:
  bog       Responds with a bog moment
  dequeue   Removes media from queue (Admin Only)
  director  Displays list of other media with the same director
  help      Shows this message
  keyword   Finds media based on a keyword
  pineapple Attempts to reset connections to fix streams. (Admin Only)
  queue     Queues Movie/TV Show to be put on Plex. If multi-worded, surround with double quotes.
  sessions  Displays what is being watched right now

Type !help command for more info on a command.
You can also type !help category for more info on a category.
```
Queue and Dequeue are features used by our group to track requests for new media to be added to the plex server.

## Future Planned Additions
- Admin ability to stop a current users stream
- If you have any suggestions please contact us and let us know