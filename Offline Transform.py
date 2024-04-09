#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This tool extracts data from all offline tournaments from a player's data.
@author: Muna N (Infernape)
"""

import pandas as pd

df = pd.read_excel("Tourney Data.xlsx")

ol = df[df['Offline'] == 1]

print(ol.info())

ol.to_excel("Offline Data.xlsx")
