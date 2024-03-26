#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
This tool provides the player with a high-level analysis of their tournament performance.
@author: Muna N (Infernape)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import operator

df = pd.read_excel("Tourney Data.xlsx")

#creating our Key Performance Indicators (KPIs)

''' 
1) Placement percentage = the proportion of the attendance pool 
you finished better than'''


df['Placement_Pct'] = 1 - df['Placement']/df['Participants']
#print(df['Placement_Pct'])

''' 
2) True Win Percentage = the number of sets you won 
divided by the total number of sets you played (wins, losses)'''

df['Set_Win_Pct'] = df['Winning_Sets']/(df['Winning_Sets'] +df['Losing_Sets'])
#print(df['True_Win_Pct'])

'''
3) Game Win Percentage = number of games you won divided by the 
total number of games you played (wins, losses)'''

df['Game_Win_Pct'] = df['Games_Won']/(df['Games_Won'] + df['Games_Lost'])
#print(df['Game_Win_Pct'])

'''
4)Set Win Ratio = the ratio between the number of sets won and the number
of sets lost'''

df['Set_Win_Rat'] = df['Winning_Sets']/(df['Losing_Sets'])
#print(df['Set_Win_Rat'])

'''
5) Game Win Ratio = the ratio between the number of games won and the number
of games lost'''

df['Game_Win_Rat'] = df['Games_Won']/(df['Games_Lost'])
#print(df['Game_Win_Rat'])

##Station for character matchups.

'''Wins/Losses --> If you beat someone game 1 and 
they switch chars and beat you, the character you beat goes into the beaten column.
If you win game 1, they don't switch, and they beat you, then that character goes 
into the loss column. Otherwise, everything else is pretty straightforward.'''

''' 
6) Characters beaten: This is the list of characters you beat in a given 
tournament, none if you didn't beat anyone.'''

w_list = []

for c in range(len(df['Chars_Won'])):
    char_w = df['Chars_Won'][c]
    if pd.isna(char_w) == False:
        char_w = char_w.split(", ")
        w_list.append(char_w)
    else:
        w_list.append(["None"])

df['Chars_Won'] = w_list

''' 
7) Characters lost to: This is the list of characters you lost to in a given 
tournament, none if you beat everyone.'''

l_list = []

for c in range(len(df['Chars_Lost'])):
    char_l = df['Chars_Lost'][c]
    if pd.isna(char_l) == False:
        char_l = char_l.split(", ")
        l_list.append(char_l)
    else:
        l_list.append(["None"])

df['Chars_Lost'] = l_list

#graphing station 1 (for target metrics)
#'''
fig, axs = plt.subplots(3,1)
fig.suptitle('SSBU Tournament Analytics')
fig.subplots_adjust(wspace= 0.3, hspace= 2)


axs[0].plot(df.Tournament, df.Placement_Pct, color = 'blue')
axs[0].scatter(df.Tournament, df.Placement_Pct, color = 'red')
axs[0].set_title('Placement Percentage')

axs[1].plot(df.Tournament, df.Set_Win_Pct, color = 'blue')
axs[1].scatter(df.Tournament, df.Set_Win_Pct, color = 'red')
axs[1].set_title('Set Win Percentage')

axs[2].plot(df.Tournament, df.Game_Win_Pct, color = 'blue')
axs[2].scatter(df.Tournament, df.Game_Win_Pct, color = 'red')
axs[2].set_title('Game Win Percentage')
#'''

df2 = df.copy(deep = True)
df2 = df2.drop(columns=['Chars_Won', 'Chars_Lost', 'Chars_All'])
corrs = df2.corr()
print(corrs)
print()

print("Average Placement Percentage:", round(np.mean(df2.Placement_Pct),3))
print("Set Win Percentage:", round(sum(df2.Winning_Sets)/(sum(df2.Winning_Sets) + sum(df2.Losing_Sets)), 3))
print("Game Win Percentage:", round(sum(df2.Games_Won)/(sum(df2.Games_Won) + sum(df2.Games_Lost)),3))
print("Average Number of Game-3+'s:", round(np.mean(df2['Game_3+']), 3))
print()

print('Tracking your KPIS and Matchup Data through', len(df['Tournament']),'tournaments:')

#graphing station 2 (for individual graphs)

'''
plt.plot(df.Tournament, df.Placement_Pct, color = 'blue')
plt.scatter(df.Tournament, df.Placement_Pct, color = 'red')
plt.ylabel('Placement Percentage')
plt.xlabel('Tournament')        
plt.show()
#'''

#character matchup analysis visualization

wins = df.Chars_Won.str.join('|').str.get_dummies().add_prefix('win_')
losses = df.Chars_Lost.str.join('|').str.get_dummies().add_prefix('loss_')

wins_dict = dict()

for chars in df['Chars_Won']:
    #print(chars)
    for c in chars:
        if c not in wins_dict:
            wins_dict[c] = 1
        else:
            wins_dict[c] += 1

#print(wins_dict)
#print()
            
losses_dict = dict()

for chars in df['Chars_Lost']:
    for c in chars:
        if c not in losses_dict:
            losses_dict[c] = 1
        else:
            losses_dict[c] += 1

#print(losses_dict)

percentage_dict = dict()

for w in wins_dict.keys():
    if w in losses_dict:
        percentage_dict[w] = round(wins_dict[w]/(wins_dict[w] + losses_dict[w]), 3)
    else:
        percentage_dict[w] = 1
        
for l in losses_dict.keys():
    if l not in wins_dict:
        percentage_dict[l] = 0
        

percentage_dict.pop('None')
sorted_p = dict(sorted(percentage_dict.items(), key = operator.itemgetter(1), reverse = True))


#Next step: using TFIDF vectorization on character data to predict KPIs

fig, ax = plt.subplots(1,1, figsize = (100,10))
fig.subplots_adjust(wspace= 80, hspace= 0.3)

plt.axhline(0.5, 0, len(sorted_p), color='red', linewidth=2, label = "50% Win Percentage")
plt.bar(sorted_p.keys(), sorted_p.values())
plt.xlabel("Character")
plt.ylabel("Win Percentage")
plt.title("Character Matchup Chart")
plt.legend()
plt.show()

print()
print(sorted_p)
