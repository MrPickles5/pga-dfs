import requests

import numpy as np
import pandas as pd

from functools import cache

import datagolf_utils as dutils



data = pd.DataFrame(res['field'])
data['r4_teetime'] = data['r4_teetime'].astype('str')

@cache
def load_field():
    url='https://feeds.datagolf.com/field-updates?tour=pga&file_format=json&key=6a626b6c312c0d33cfe157d614b5'
    players = request.get(url).json()['field']
    for player in players:
        players['player_name'] = dutils.clean_name(player['player_name'])
    return players

@cache
def load_field_made_cut():
    field = load_field()
    return dict(filter( field[k]['r4_teetime']!='None' for k,v in field.items() ))
    

def players_frame(cut=False):
    if cut:
        return pd.DataFrame( load_field_made_cut() )
    return pd.DataFrame( load_field() )
    
made_cut = data.loc[data['r4_teetime']!='None'].reset_index(drop=True) #*
made_cut['player_name'] = made_cut['player_name'].astype('str')


made_cut['name'] = made_cut['player_name'].apply( dutils.clean_name )

def players_who_made_cut():
    return( tuple(made_cut['name'].values.tolist()) )

proj_url='https://feeds.datagolf.com/preds/fantasy-projection-defaults?tour=pga&site=draftkings&slate=showdown&file_format=json&key=6a626b6c312c0d33cfe157d614b5'
pres = requests.get(proj_url).json()

proj=pd.DataFrame(pres['projections'])
proj['name'] = proj['player_name'].apply( dutils.clean_name )
proj=proj.loc[:,['name','proj_points']]
proj.index=proj['name']
proj=proj.drop('name', axis=1)
proj.to_pickle('../data/pickle-buffer/proj-pts.pkl')

def proj_pts(name):
    return(proj.loc[name,'proj_points'] if name in proj.index else 0.0)