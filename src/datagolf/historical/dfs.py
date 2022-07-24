import pandas as pd

from ..devtools.aux import Clean
from ..devtools.api_tools import URL
from picklejar import PickleJar


class DFS:
    
    drop = ['dg_id', 'ownership']
    
    requirements = {
        'tour': 'pga',
        'years': (2021, 2022),
    }
    
    # pnames = tuple(PickleJar.load('fanduel')['name'].values.tolist())
    
    @classmethod
    def event_ids(cls):
        events = URL.historical_event_ids() # List of dicts
        
        ret = tuple(filter( lambda d: d['calendar_year'] in cls.requirements['years'] and d['tour']==cls.requirements['tour'], events ))
        
        return ret
    
    
    @classmethod
    def load(cls, event_id=100):
        
        results = Clean.names( URL.historical_dfs(event_id) ) # event_id is only param --> List of result dicts for each player from event
        
        ret = (pd.DataFrame(results)
               .rename({'player_name': 'name', 'fin_text': 'placement'}, axis=1)
               .drop(cls.drop, axis=1)
              )
        ret.columns = ret.columns.str.replace('_pts','')
        
        first = ['name', 'placement']
        order = first + list(filter(lambda x: x not in first, list(ret.columns)))
        
        ret = ret.loc[:, order]
        return ret