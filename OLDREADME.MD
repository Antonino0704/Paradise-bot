# Paradise bot

   A bot whose main function is to speak instead of someone who can't speak

   It also has other features like a dummy system of game coins, sending embed messages or [play music](#known-bugs) &#x2612;

   Default prefix = $
    
# News
## Fixed Bugs
   * Fixed the name of list in the queue bug
   * Fixed Updating the name of guilds in the database when these changed
   * Fixed Unsupported emoji bug (guilds name support emoji characters)
   * Fixed Crash of info when it was too long
## All slash commands

   * ### Will the old commands receive updates?
      >No, they won't no longer be supported and they won't receive updates
    
 
# Known bugs
   - third party service has problems, songs on youtube are temporarily suspended 
   - if the bot doesn't connect to your server use the $clean command and try again (it may be necessary to try several times)
    
# Bugs
   if you find a bug open a new issue on github
    
    
# Setup project
  ## You must already have them installed:
   >[Python 3(3.9 recommended)](https://www.python.org/downloads/)\
   >[Git](https://git-scm.com/downloads)\
   >[MariaDB](https://mariadb.org/download/?t=mariadb&p=mariadb&r=10.11.2)\
   >[FFmpeg](https://ffmpeg.org/download.html)\
   >[NodeJS](https://nodejs.org/en/download)
   
  [create a bot account](https://discordpy.readthedocs.io/en/stable/discord.html)\
  fork the project\
  start your MariaDB server
  >Linux:  ```systemctl start mysql```\
  >Windows: go to MariaDB folder (it is usually in C:\Program Files\MariaDB\bin) and double click on mysql.exe
  
  open a terminal where you prefer
  ## Type these commands:
     git clone your fork link
     python -m venv venv
     
  Linux: ```source venv/bin/activate```\
  Windows: ```venv/Scripts/activate```\
  ```cd Paradise-bot```\
  create the database: ```mysql < paradiseDatabase.sql```\
  install the requirements: ```pip install -r requirements.txt``` and  ```npm i```\
  create a .env file and write into it:
  >token=YourAppToken\
  >address=YourMariaDBServerAddress\
  >usr=YourMariaDBServerUsername\
  >passwd=YourMariaDBServerPassword\
  >songs=PathYourSavedSongsFolder\
  >ffmpeg=PathFFmpegFolder
  
  run the bot:  ```python Paradise.py```


# Author
   [Antonino Buscarino](https://beacons.ai/_hikki_)
