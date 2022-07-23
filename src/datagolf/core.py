import requests

import numpy as np
import pandas as pd

from functools import cache

from .devtools.aux import Clean
from .devtools.api_tools import URL
from .modeling.skills import Decompose, Rating
from .modeling.dfs import Projections
from .modeling.baselines import Baselines


class datagolf:
    @cache
    def load_field():
        url='https://feeds.datagolf.com/field-updates?tour=pga&file_format=json&key=6a626b6c312c0d33cfe157d614b5'
        players=request.get(url).json()['field']
        return Clean.names(players)

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

    def load_dfs():
        
        fd = Projections.load('pga', 'fanduel', 'main', 'json')
        dk = Projections.load('pga', 'draftkings', 'main', 'json')
        
        dk = dk.rename({'ownership': 'dk-ownership'}, axis=1)
        ret = pd.concat([fd, dk['dk-ownership']], axis=1)
        
        ret = ret.drop('ownership', axis=1)
        ret = ret.rename({'dk-ownership': 'ownership'}, axis=1)
        
        return ret

    def load_skills(decomp=True, tidy=True):
        return Decompose.load('pga', 'json', tidy=tidy) if decomp else Rating.load('value', 'json', tidy=tidy)
    
    def load_baselines(tidy=True):
        return Baselines.load('pga', '2,3,4,5', 'percent', 'json', tidy=tidy)