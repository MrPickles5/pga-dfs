import pandas as pd

from picklejar import PickleJar

class PGA:
    
    components = {
        'tee': { 'url-id': 2567, 'sg-id': 'ott' },
        'approach': { 'url-id': 2568, 'sg-id': 'app' },
        'around': { 'url-id': 2569, 'sg-id': 'arg' },
        'green': { 'url-id': 2564, 'sg-id': 'putt' },
        'tee-to-green': { 'url-id': 2674, 'sg-id' : 'ttg' }
    }
    
    rename = {
        'player name': 'name',
        'rank this week': ' cur-rank',
        'rank last week': ' prev-rank',
        'average': ' sg',
        'rounds': ' num-rounds',
        'measured rounds': ' num-measured'
    }
    
    pga_root = 'https://www.pgatour.com/stats/stat.0{}.html'
    
    @classmethod
    def strokes_gained_from(cls, component, abbreviate=True):
        
        if component.lower() not in cls.components:
            print('ERROR: Enter valid strokes gained component:... \n')
            return None
        
        ret = pd.read_html(cls.pga_root.format(cls.components[component]['url-id']))[1].reset_index(drop=True)
        
        ret.columns = ret.columns.str.lower().str.replace('total sg:', ' sg').str.replace('\xa0', ' ')
        ret = ret.rename(cls.rename, axis=1)
        
        if abbreviate:
            ret = ret.loc[:, ('name', ' sg')]
            
        ret.columns = ret.columns.str.replace(' ', f'{cls.components[component]["sg-id"]}-')

        PickleJar.prepare(ret, 'strokes', fparam=component)
        
        return None
    
    @classmethod
    def strokes_gained(cls):
        frames = dict()# Update and pickle
        for component in cls.components:
            cls.strokes_gained_from(component)
            frames.update({ component: PickleJar.load('strokes', fparam=component) })
            
        # Initialize frame as tee and merge
        strokes = frames['tee']
        for k in list(cls.components.keys())[1:]:
            strokes = strokes.merge(frames[k])
            
        PickleJar.prepare( strokes.reset_index(drop=True) ,'strokes' )
        return None
        
    @classmethod
    def StrokesGained(cls):
        cls.strokes_gained()
        return PickleJar.load('strokes')
                
            
                