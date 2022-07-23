import requests

import numpy as np
import pandas as pd

from functools import cache

from ..devtools.aux import Clean
from ..devtools.api_tools import URL
from picklejar import PickleJar


class Rankings:
    
    renaming = {
        'player_name': 'name',
        'datagolf_rank': 'dg-rank',
        'dg_skill_estimate': 'skill-estimate',
        'owgr_rank': 'owgr-rank',
        'primary_tour': 'tour'
    }
    
    @classmethod
    def load(cls,file_format):
        ret = (pd
               .DataFrame(URL.datagolf_rankings(file_format), columns=cls.renaming.keys())
               .rename(cls.renaming, axis=1)
              )
        
        return ret
        