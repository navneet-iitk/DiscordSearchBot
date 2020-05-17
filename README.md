# DiscordSearchBot
Discord Bot to help user do google search in discord servers. Built using discord.py python package 
and Redis as in memory database.

The whole project has been dockerized.

Project requires the Discord Bot token (acquired after creating discord application and bot at 
Discord Developer portal - https://discord.com/developers/applications)

Commands (With command prefix as - '!') :-
!google <keyword> 
  Gives top 5 links found on searching for given keyword at Google

!recent <keyword>
  Gives top 5 recent queries made by an user.
  'keywod' is optional. If provided, results with partial matching done on queries with given keyword are returned,
  else, just the top 5 recent onces are returned.
