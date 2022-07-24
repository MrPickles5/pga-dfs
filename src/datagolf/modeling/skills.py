import requests

import numpy as np
import pandas as pd

from functools import cache

from ..devtools.aux import Clean
from ..devtools.api_tools import URL
from picklejar import PickleJar


class CourseFit:
    
    renaming = {
        'player_name': 'name',
        'baseline_pred': 'baseline',
        'final_pred': 'final',
        'strokes_gained_category_adjustment': 'category-sg',
        'true_sg_adjustments': 'true-sg',
        'driving_accuracy_adjustment': 'driving-accuracy',
        'total_fit_adjustment': 'total-fit'
    }
    
    
    @classmethod
    def load(cls, tidy=True):
        ret = (pd
               .DataFrame(URL.skills_decomp(), columns=cls.renaming.keys())
               .rename(cls.renaming, axis=1)
              )
        
        return Clean.columns(ret) if tidy else URL.skills_decom()
    
    
class Breakdown:
    
    renaming = {
        'player_name': 'name',
        'driving_acc': 'drv-acc',
        'driving_dist': 'drv-dist',
        'sg_app': 'sg-app',
        'sg_arg': 'sg-arg',
        'sg_ott': 'sg-ott',
        'sg_putt': 'sg-putt',
        'sg_total': 'sg-total'
    }
    
    pnames = tuple(PickleJar.load('fanduel')['name'].values.tolist())
    
    @classmethod
    def load(cls, tidy=True):
        df = (pd
              .DataFrame(URL.skills_rating(), columns=cls.renaming.keys())
              .rename(cls.renaming, axis=1)
             )
        
        ret = (df
               .loc[ df['name'].isin(cls.pnames) ]
               .reset_index(drop=True)
              )
        
        return Clean.columns(ret) if tidy else URL.skills_rating()
        