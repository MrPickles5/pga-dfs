import requests

import numpy as np
import pandas as pd

from functools import cache

from .devtools.aux import Clean
from .devtools.api_tools import URL
from .modeling.skills import Breakdown, CourseFit
from .modeling.dfs import Projections
from .modeling.baselines import Baselines
from .modeling.rankings import Rankings


class DataGolf:
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

    def dfs():
        
        fd = Projections.load('fanduel')
        dk = Projections.load('draftkings')
        
        dk = dk.rename({'ownership': 'dk-ownership'}, axis=1)
        ret = pd.concat([fd, dk['dk-ownership']], axis=1)
        
        ret = ret.drop('ownership', axis=1)
        ret = ret.rename({'dk-ownership': 'ownership'}, axis=1)
        
        return Clean.columns(ret)

    def skills(general=True, tidy=True):
        return Breakdown.load(tidy=tidy) if general else CourseFit.load(tidy=tidy)
    
    def baselines(tidy=True):
        return Baselines.load()
    
    def rankings():
        return Rankings.load()