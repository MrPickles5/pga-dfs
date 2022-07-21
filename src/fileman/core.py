import os
import pandas as pd

import constants

class fileman:
#     Class attributes
    
    root = os.getcwd().replace('src','data/') #+'pickle-buffer/'
    
    csv_fs = root+'contest-files/'
    pkl_fs = root+'pickle-buffer/'
    
    shorten = {'tee': 'ott', 'approach': 'app', 'around': 'arg', 'green': 'putt', 'tee-to-green': 'ttg'}
    paths = {
        
        'fanduel': {
            'csv': f'{constants.tournament}.csv',
            'pkl': 'fanduel-data.pkl'
        },
        
        'strokes' : {
            'component': 'sg-{}.pkl', #.format()
            'pkl': 'strokes-gained.pkl'
        },
        
        'optimizer': {
            'raw': 'optimizer-raw.pkl',
            'clean': 'optimizer-clean.pkl'
        }
    }
    
    @classmethod
    def fanduel(cls, param=None):
        return cls.pkl_fs + cls.paths['fanduel']['pkl'] if param is None else cls.csv_fs + cls.paths['fanduel']['csv']
    
    @classmethod
    def strokes_gained(cls, param=None):
        return cls.pkl_fs + cls.paths['strokes']['pkl'] if param is None else cls.pkl_fs + cls.paths['strokes']['component'].format(cls.shorten.get(param,param))
    
    @classmethod
    def optimizer(cls, param=None):
        return cls.pkl_fs + cls.paths['optimizer'][f'{"clean" if param is None else "raw"}']
    
    @classmethod
    def getfs(cls, ftype, fparam):
        
        if ftype == 'created':
            return cls.root + f'lineups-created/{constants.tournament}.pkl'
        
        elif ftype == 'combined':
            return cls.pkl_fs + 'combined.pkl'
        
        elif ftype == 'strokes' and fparam is not None:
            return cls.strokes_gained(fparam)
        
        return {'fanduel': cls.fanduel(fparam), 'strokes': cls.strokes_gained(fparam), 'optimizer': cls.strokes_gained(fparam)}.get(ftype, None)
    
