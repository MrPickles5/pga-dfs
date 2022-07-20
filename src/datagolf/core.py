import requests

import numpy as np
import pandas as pd

from functools import cache

from .devtools.aux import Clean


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

    @cache
    def load_projections():
        url='https://feeds.datagolf.com/preds/fantasy-projection-defaults?tour=pga&site=fanduel&slate=main&file_format=json&key=6a626b6c312c0d33cfe157d614b5'
        players = requests.get(url).json()['projections']
        return Clean.names(players)

    def pickle_projections():

        df=(pd
            .DataFrame( load_projections(), columns=('player_name', 'proj_points') )
            .rename({'player_name': 'name', 'proj_points': 'proj-pts'}, axis=1)
           )

        ret = Clean.columns(df)
        ret.to_pickle('../data/pickle-buffer/proj-pts.pkl')

        # Clean.columns(df).to_pickle('../data/pickle-buffer/proj-pts.pkl')

        return None


    def preview():
        return pd.read_pickle('../data/pickle-buffer/proj-pts.pkl').head(10)

    def proj_pts(name):
        pts=pd.read_pickle('../data/pickle-buffer/proj-pts.pkl')
        pts.index=pts['name']
        pts=pts.drop('name', axis=1)
        return pts.loc[name,'proj-pts'] if name in pts.index else 0.0


    @cache
    def load_skills_decomp():
        url='https://feeds.datagolf.com/preds/player-decompositions?tour=pga&file_format=json&key=6a626b6c312c0d33cfe157d614b5'
        players=requests.get(url).json()['players']
        for player in players:
            player['player_name'] = Clean.name( player['player_name'] )
        return players

    def pickle_skills():

        df = (pd
              .DataFrame( load_skills_decomp(), columns=('player_name', 'final_pred') )
              .rename({'player_name': 'name', 'final_pred': 'cfit-adj'}, axis=1)
             )

        ret = Clean.columns(df)
        ret.to_pickle('../data/pickle-buffer/skills-decomp.pkl')

        return None

    def proj_skd(name):
        skd=pd.read_pickle('../data/pickle-buffer/skills-decomp.pkl')
        skd.index=skd['name']
        skd=skd.drop('name', axis=1)
        return skd.loc[name, 'cfit-adj'] if name in skd.index else 0.0

    def startup():
        pickle_projections()
        pickle_skills()