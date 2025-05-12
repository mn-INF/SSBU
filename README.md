
![BreakDance](https://github.com/user-attachments/assets/a9179fc1-577f-4383-a85b-f96ea5a5ba33)

SSBU: High Level Tournament Analytics 
(A Product by Infernape)

This tool provides the player with a high-level analysis of their tournament performance. By filling out the spreadsheet template and running the code attached in this package, a player can view KPIs and specific character matchup data from their past online and offline tournaments (most if not all of this can be found on https://smashdata.gg/ and typing in your previous player tags). The goal of this is not only an exercise in gathering/visualizing your data, but also for players to have an even more granular view of their results and performance against certain characters.

In addition to the main script (Tourney Analysis.py), this git repo (https://github.com/mn-INF/SSBU.git) contains a spreadsheet of my data as an example (Tourney Data.xlsx). There is also a blank template (Tourney Data Template.xlsx), in addition to a helper script that pulls your offline data (Offline Transform.py) and saves that data into its own table (Offline Data.xlsx) and a secondary script that calculates your chances of qualifying for top 8 at a tournament, with a given bracket path of characters (Bracket Calc.py). The bracket calculation script also saves the model in a .pkl file to enable predictions via Flask API.

General Information for Filling Out the Template

•	Tournament → Index stating the number of the tournament entered
•	Placement → Your placement in the tournament
•	Participants → The number of participants in the tournament
•	DQ_Wins → The number of sets you win via DQ
•	Winning_Sets → The number of sets you win in a tournament
•	Losing_Sets → The number of sets you lose in a tournament
•	Games_Won → The number of games you win in a tournament
•	Games_Lost → The number of games you lose in a tournament
•	Game_3+ → The number of sets you play in a tournament that go to game 3 or higher
•	Sweeps → The number of sets you play in a tournament that are either 2-0 or 3-0 (either in your favor or against you)
•	Chars_Won → This is the list of characters you beat in a tournament, None if you didn't beat anyone
•	Chars_Lost  → This is the list of characters you lost to in a tournament, None if you beat everyone
•	Tourney_Win → This indicates whether you won the tournament or not
•	Offline → This indicates whether the tournament played was offline or not
•	Top_8 → This indicates whether or not the player made Top 8 at this bracket

* Criteria for wins and Losses: If you beat someone game 1 and they switch characters to win the set, the character you beat goes into the beaten column. If you win game 1, they don't switch, and they win the set, then that goes into the loss column. Otherwise, everything else is pretty straightforward.
  
KPIs

Key Performance Indicators (KPIs) are the main metrics that are used to determine overall tournament performance. They are:

•	Placement_Pct → Placement Percentage is the percentage of the participants in a tournament than which you did better
•	Set_Win_Pct → Set Win Percentage is the percentage of sets you won in a tournament
o	Winning_Sets/(Winning_Sets + Losing_Sets)
•	Game_Win_Pct → Game Win Percentage is the percentage of games you won in a tournament
o	Games_Won/(Games_Won + Games_Lost)
•	Set_Win_Rat → Set Win Ratio is the ratio between the number of sets won and sets lost (ex. A set_win_rat of 1 implies that you went 2-2 at a tournament)
o	Winning_Sets/Losing_Sets
•	Game_Win_Rat → Game Win Ratio is the ratio between the number of games won and games lost
o	Games_Won/Games_Lost

•	Placement_Pct, Set_Win_Pct, and Game_Win_Pct are all displayed in the form of a line graph.

Character Matchups

•	The characters you beat and lost to are able to be visualized by running the attached code in the folder. These visualize every character you played against your win percentages against those characters.
•	For offline tournaments you just need to remember what characters your opponent played.
•	This streamlines the process of figuring out which characters you do well against and which ones need more attention in terms of matchup experience.

Next Steps

Right now, the tournament data has to be input manually into a spreadsheet with the column names above as a template. I’m not sure if there is a way to automate the data collection, but I’ll keep looking into that. I hope this makes the improvement process easier!

Housekeeping

•	To analyze your data, make sure you have the most recent version of Python downloaded, and an application that provides you with an IDE to run the code. 
•	When you download everything, be sure to keep the Python files and the spreadsheets all in the same folder/directory.
•	Within the quotation marks on any read_excel() calls, put the name of your spreadsheet. This is whatever you save the Excel spreadsheet as, but make sure to keep it in .xlsx format.
•	For recording the characters used against you, be sure to follow the criteria above.
•	To track an individual stat, you can just remove the apostrophes around lines 132-136 in Tourney Analysis.py. To make sure that it doesn’t get displayed, put 3 apostrophes before line 132 and 3 more after line 136.
