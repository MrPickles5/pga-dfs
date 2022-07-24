import os
import requests

import numpy as np
import pandas as pd
from functools import cache

# Passed as default to all currently --> Tuple because should never pass mutable objects into default arguments
from .auth import DATAGOLF_KEY
from .aux import Clean

class URL:

    urls = {
        'course-fit': 'https://feeds.datagolf.com/preds/player-decompositions?tour={tour}&file_format={file_format}&key={key}',
        'strokes-gained': 'https://feeds.datagolf.com/preds/skill-ratings?display={display}&file_format={file_format}&key={key}',
        'dfs-projections': 'https://feeds.datagolf.com/preds/fantasy-projection-defaults?tour={tour}&site={site}&slate={slate}&file_format={file_format}&key={key}',
        'pre-predictions': 'https://feeds.datagolf.com/preds/pre-tournament?tour={tour}&add_position={add_position}&odds_format={odds_format}&file_format={file_format}&key={key}',
        'rankings': 'https://feeds.datagolf.com/preds/get-dg-rankings?file_format={file_format}&key={key}',
        
# * --> Does not work during events
        'betting-odds': 'https://feeds.datagolf.com/betting-tools/outrights?tour={tour}&market={market}&odds_format={odds_format}&file_format={file_format}&key={key}',
        
# * --> Need annual subscription for following:
        'historical-event-ids': 'https://feeds.datagolf.com/historical-dfs-data/event-list?file_format={file_format}&key=6a626b6c312c0d33cfe157d614b5',
        'historical-dfs': 'https://feeds.datagolf.com/historical-dfs-data/points?tour={tour}&site={site}&event_id={event_id}&year={year}&file_format={file_format}&key={key}',
        'historical-raw': 'https://feeds.datagolf.com/historical-raw-data/rounds?tour={tour}&event_id={event_id}&year={year}&file_format={file_format}&key={key}'
    }
    
    key = DATAGOLF_KEY
    
    # Done this way to better configure defaults later --> **kwargs
    params = {
        'add_position': '2,3,4,5',
        'display': 'value',
        'file_format': 'json',
        'market': 'make_cut', #'win, top_5, top_10, top_20, mc, make_cut',
        'odds_format': 'percent',
        'site': 'fanduel',
        'slate': 'main',
        'tour': 'pga',
        'year': '2022'
    }
    
    

    @classmethod
    @cache
    def course_fit(cls):
        url = cls.urls['course-fit'].format(tour=cls.params['tour'], file_format=cls.params['file_format'], key=cls.key)
        return Clean.names( requests.get(url).json()['players'] )

    @classmethod
    @cache
    def strokes_gained(cls):
        url = cls.urls['strokes-gained'].format(display=cls.params['display'], file_format=cls.params['file_format'], key=cls.key)
        return Clean.names( requests.get(url).json()['players'] )

    @classmethod
    @cache
    def dfs_projections(cls, site):
        url = cls.urls['dfs-projections'].format(tour=cls.params['tour'], site=site, slate=cls.params['slate'], file_format=cls.params['file_format'], key=cls.key)
        # if site is not None:
        #     url = url.replace('fanduel', 'draftkings')
        return Clean.names( requests.get(url).json()['projections'] )

    @classmethod
    @cache
    def pretournament_predictions(cls):
        url = cls.urls['pre-predictions'].format(tour=cls.params['tour'], add_position=cls.params['add_position'], odds_format=cls.params['odds_format'], file_format=cls.params['file_format'], key=cls.key)
        return Clean.names( requests.get(url).json()['baseline'] )
    
    @classmethod
    @cache
    def datagolf_rankings(cls):
        url = cls.urls['rankings'].format(file_format=cls.params['file_format'], key=cls.key)
        return Clean.names( requests.get(url).json()['rankings'] )
    
    @classmethod
    @cache
    def betting_odds(cls):
        url = cls.urls['betting-odds'].format(tour=cls.params['tour'], market=cls.params['market'], odds_format=cls.params['odds_format'], file_format=cls.params['file_format'], key=cls.key)
        # return Clean.names(requests.get(url).json())
        return requests.get(url).json()
    
    @classmethod
    @cache
    def historical_event_ids(cls):
        url = cls.urls['historical-event-ids'].format(file_format=cls.params['file_format'])
        return requests.get(url).json()
    
    
    @classmethod
    @cache
    def historical_dfs(cls, event_id):
        url = cls.urls['historical-dfs'].format(tour=cls.params['tour'], site=cls.params['site'], event_id=event_id, year=cls.params['year'], file_format=cls.params['file_format'], key=cls.key)
        return requests.get(url).json()['dfs_points']
    
    @classmethod
    @cache
    def historical_raw(cls):
        url = cls.urls['historical-raw'].format(tour=cls.params['tour'], event_id='all', year=cls.params['year'], file_format=cls.params['file_format'], key=cls.key )
        return requests.get(url).json()


