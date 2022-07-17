import requests

import numpy as np
import pandas as pd

url='https://feeds.datagolf.com/field-updates?tour=pga&file_format=json&key=6a626b6c312c0d33cfe157d614b5'
res = requests.get(url).json()

data = pd.DataFrame(res['field'])
data['r4_teetime'] = data['r4_teetime'].astype('str')

made_cut = data.loc[data['r4_teetime']!='None'].reset_index(drop=True)
made_cut['player_name'] = made_cut['player_name'].astype('str')

def clean_name(name):
    if len(name.split(' '))==2:
        parts=name.replace(' ', '').split(',')
        return(' '.join([parts[1],parts[0]]))
    else:
        parts=name.replace(',', '').split(' ')
        return(' '.join([parts[1], parts[2], parts[0]]))
    

made_cut['name'] = made_cut['player_name'].apply( clean_name )

def players_who_made_cut():
    return( tuple(made_cut['name'].values.tolist()) )