import pandas as pd

from tqdm.notebook import tqdm

from ..devtools.aux import Clean
from ..devtools.api_tools import URL
from picklejar import PickleJar

class Raw:

    rawdata = URL.historical_raw()
    event_ids = tuple(rawdata.keys())
    
    @staticmethod
    def format_event_name(event):
        return event.replace('The ', '').lower().replace(' ', '-').replace('&', '')
    
    @classmethod
    def pull(cls):
        
        for eid in tqdm(cls.event_ids):
            event = cls.rawdata[eid]['event_name']
            event_fname = cls.format_event_name(event)
            
            frames=list()
            
            for results in cls.rawdata[eid]['scores']:
                
                name = Clean.name( results['player_name'] )
                placement = results['fin_text']
                
                rounds = list(filter(lambda x: 'round' in x, results.keys()))
                event_data = list(map( lambda x: results[x], rounds ))
            
                df = pd.DataFrame(event_data)
                df['name'] = name
                df['placement'] = placement
                
                first = ['name', 'placement']
                order = first + list(filter(lambda x: x not in first, df.columns))
                
                df = df.loc[:, order]
                frames.append(df)
            
            ret = pd.concat(frames).reset_index(drop=True)
            
            PickleJar.prepare(ret, 'datagolf', event_fname)
            
        
        return None
    
    
    @classmethod
    def preview(cls, num=100):
        
        frames=list()
        for eid in cls.event_ids:
            
            event = cls.rawdata[eid]['event_name']
            event_fname = cls.format_event_name(event)
            
            frames.append( PickleJar.load('datagolf', event_fname) )
            
        ret = pd.concat(frames).reset_index(drop=True)
        
        return ret.head(num)