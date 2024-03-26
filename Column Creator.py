#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 14:32:48 2023

@author: default
"""
import pandas as pd

df = pd.read_excel('Tourney Data.xlsx')

alls = []

for i in range(len(df)):
    all_str = df['Chars_Won'][i] + ', ' + df['Chars_Lost'][i]
    all_str = all_str.replace('None,', '')
    all_str = all_str.replace('None', '')
    alls.append(all_str)

#print(alls)

df['Chars_All'] = alls

#df.to_excel('Tourney Data.xlsx')