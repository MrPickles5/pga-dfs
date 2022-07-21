# Cleaner name than pre_tournament_predicitions

import requests

import numpy as np
import pandas as pd

from functools import cache

from ..devtools.aux import Clean
from ..devtools.api_tools import URL
from picklejar import PickleJar


class Baselines:

    renaming = {
        'player_name': 'name',
        'make_cut': 'make-cut',
        'win': '1st(%)',
        'top_2': '2nd(%)',
        'top_3': '3rd(%)',
        'top_10': 'top-10(%)',
        'top_20': 'top-20(%)'
    }
    
    @classmethod
    def load(cls, tour, add_position, odds_format, file_format, tidy=True):
        ret = (pd
               .DataFrame(URL.pretournament_predictions(tour, add_position, odds_format, file_format), columns=cls.renaming.keys())
               .rename(cls.renaming, axis=1)
              )
        
        return ret if tidy else URL.pretournament_predictions(tour, add_position, odds_format, file_format)