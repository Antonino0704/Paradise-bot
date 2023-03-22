# Paradise server's official bot

   A bot whose main function is to speak instead of someone who can't speak

   It also has other features like a dummy system of game coins, sending embed messages or play music

   Default prefix = $
   
   ⚠The voice commands aren't working⚠
    
# Development Status
   I created this bot because not everyone can talk in voice chat but I'm alone in development and between high school final exam, driving license exam and college tests 
   I don't have enough time. This is not my job and not get any salary 
    so at moment the bot will not receive any updates and development status is suspended.

# Start:
   Don't waste time with permissions, the bot is safe:

    https://discord.com/api/oauth2/authorize?client_id=1004801168674926643&permissions=8&scope=bot

   Doesn't feel trust worthy? here is another link with the minimum permissions needed

    https://discord.com/api/oauth2/authorize?client_id=1004801168674926643&permissions=412622519376&scope=bot

   type $help to learn all commands
    
# News
## A new save system
   The bot now has a database (the old save system was deleted and replaced by a database server) 

## Fixed bugs
   The bug that didn't give cats after buying them was fixed

   fixed the bug that would make coin payments even if you were not blacklisted in the Rban command

## New commands
   $setFirstLastName command -> allows you to set a first and last name for the account

   $infoItem -> shows item information
   $infoBadge -> shows badge information
   $infoJob -> shows job information

## Coins
   Decreased the odds of finding a coin, from 10% to 1%

    
 
# Known bugs
   if the bot doesn't connect to your server use the $clean command and try again (it may be necessary to try several times)
    
# Bugs
   if you find a bug open a new issue on github
    
    
# Setup project
  ## You must already have them installed:
   >[Python 3(3.9 recommended)](https://www.python.org/downloads/)\
   >[Git](https://git-scm.com/downloads)\
   >[MariaDB](https://mariadb.org/download/?t=mariadb&p=mariadb&r=10.11.2)\
   >[FFmpeg](https://ffmpeg.org/download.html)
   
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
  install the requirements: ```pip install -r requirements.txt```\
  create a .env file and write into it:
  >token=YourAppToken\
  >address=YourMariaDBServerAddress\
  >usr=YourMariaDBServerUsername\
  >passwd=YourMariaDBServerPassword\
  >songs=PathYourSavedSongsFolder\
  >ffmpeg=PathFFmpegFolder
  
  run the bot:  ```python Paradise.py```
  
  
# Author
    Antonino Buscarino
    https://twitter.com/Hikki0704
    https://t.me/han_ako0
    https://notbeenoughsocial.pythonanywhere.com/profile/hikki/
    https://techhub.social/@Hikki
