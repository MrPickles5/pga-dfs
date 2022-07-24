import requests

import numpy as np
import pandas as pd

from functools import cache

from ..devtools.aux import Clean
from ..devtools.api_tools import URL
from picklejar import PickleJar


class Projections:
    
    renaming = {
        'player_name': 'name',
        'salary': 'salary',
        'proj_ownership': 'ownership',
        'proj_points': 'points',
        'early_late_wave': 'later'
    }
    
    @classmethod
    def load(cls, site):
        ret = (pd
               .DataFrame(URL.dfs_projections(site), columns=cls.renaming.keys())
               .rename(cls.renaming, axis=1)
               .reset_index(drop=True)
              )
        
        return ret
        