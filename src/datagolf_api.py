import requests

import numpy as np
import pandas as pd

from functools import cache

import datagolf_utils as dutils

@cache
def ctype(c):
    return {'name': 'str', 'proj-pts': 'float'}.get(c, 'str')

@cache
def load_field():
    url='https://feeds.datagolf.com/field-updates?tour=pga&file_format=json&key=6a626b6c312c0d33cfe157d614b5'
    players=request.get(url).json()['field']
    for player in players:
        player['player_name'] = dutils.clean_name( player['player_name'] )
    return players

@cache
def load_field_made_cut():
    field=load_field()
    return dict( filter( field[k]['r4_teetime']!='None' for k,v in field.items() ) )
    

def players_frame(cut=False):
    if cut:
        return pd.DataFrame( load_field_made_cut() )
    return pd.DataFrame( load_field() )

def players_who_made_cut():
    return tuple(made_cut['name'].values.tolist())

@cache
def load_projections():
    url='https://feeds.datagolf.com/preds/fantasy-projection-defaults?tour=pga&site=fanduel&slate=main&file_format=json&key=6a626b6c312c0d33cfe157d614b5'
    players=requests.get(url).json()['projections']
    for player in players:
        player['player_name']=dutils.clean_name(player['player_name'])
    return tuple(players)

def pickle_projections():
    
    df=(pd
        .DataFrame( load_projections(), columns=('player_name', 'proj_pts') )
        .rename({'player_name': 'name', 'proj_pts': 'proj-pts'}, axis=1)
       )
    
    for c in df.columns:
        df[c]=df[c].astype(ctype(c))
    
    print(df.head())
    
    df.to_pickle('../data/pickle-buffer/proj-pts.pkl')
    
    return None

pickle_projections()
    
    
def preview():
    return pd.read_pickle('../data/pickle-buffer/proj-pts.pkl').head(10)

def proj_pts(name):
    proj=pd.read_pickle('../data/pickle-buffer/proj-pts.pkl')
    proj.index=proj['name']
    proj=proj.drop('name', axis=1)
    return proj.loc[name,'proj-pts'] if name in proj.index else 0.0