import os
import requests

import numpy as np
import pandas as pd
from functools import cache

from .aux import Clean

class URL:

    urls = {
        'skills-decomp': 'https://feeds.datagolf.com/preds/player-decompositions?tour={tour}&file_format={file_format}&key=6a626b6c312c0d33cfe157d614b5',
        'skills-rating': 'https://feeds.datagolf.com/preds/skill-ratings?display={display}&file_format={file_format}&key=6a626b6c312c0d33cfe157d614b5',
        'dfs-projections': 'https://feeds.datagolf.com/preds/fantasy-projection-defaults?tour={tour}&site={site}&slate={slate}&file_format={file_format}&key=6a626b6c312c0d33cfe157d614b5',
        'pre-predictions': 'https://feeds.datagolf.com/preds/pre-tournament?tour={tour}&add_position={add_position}&odds_format={odds_format}&file_format={file_format}&key=6a626b6c312c0d33cfe157d614b5'
    }

    @classmethod
    @cache
    def skills_decomp(cls, tour, file_format):
        url = cls.urls['skills-decomp'].format(tour=tour, file_format=file_format)
        return Clean.names( requests.get(url).json()['players'] )

    @classmethod
    @cache
    def skills_rating(cls, display, file_format):
        url = cls.urls['skills-rating'].format(display=display, file_format=file_format)
        return Clean.names( requests.get(url).json()['players'] )

    @classmethod
    @cache
    def dfs_projections(cls, tour, site, slate, file_format):
        url = cls.urls['dfs-projections'].format(tour=tour, site=site, slate=slate, file_format=file_format)
        return Clean.names( requests.get(url).json()['projections'] )

    @classmethod
    @cache
    def pretournament_predictions(cls, tour, add_position, odds_format, file_format):
        url = cls.urls['pre-predictions'].format(tour=tour, add_position=add_position, odds_format=odds_format, file_format=file_format)
        return Clean.names( requests.get(url).json()['baseline'] )


