import pandas as pd

from ..devtools.aux import Clean
from ..devtools.api_tools import URL
from picklejar import PickleJar

class BettingOdds:
    
    # renaming = {
    #     'player_name': 'name',
    #     'driving_acc': 'drv-acc',
    #     'driving_dist': 'drv-dist',
    #     'sg_app': 'sg-app',
    #     'sg_arg': 'sg-arg',
    #     'sg_ott': 'sg-ott',
    #     'sg_putt': 'sg-putt',
    #     'sg_total': 'sg-total'
    # }
    
    pnames = tuple(PickleJar.load('fanduel')['name'].values.tolist())
    
    @classmethod
    def load(cls, tidy=True):
        df = (pd
              .DataFrame(URL.betting_odds() ) #, columns=cls.renaming.keys())
              # .rename(cls.renaming, axis=1)
             )
        
        return df