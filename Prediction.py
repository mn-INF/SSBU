#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 02:14:50 2024

@author: mnwana
"""

import pickle
import pandas as pd
import json

def predict_run(config):
    ##loading the model from the saved file
    pkl_filename = "model.pkl"
    with open(pkl_filename, 'rb') as f_in:
        model = pickle.load(f_in)

    if type(config) == dict:
        df = pd.DataFrame(config)
    else:
        df = config
    
    y_pred = model.predict(df['Chars_All'])
    
    if y_pred == 0:
        return 'Will not make top 8'
    elif y_pred == 1:
        return 'Will make top 8'