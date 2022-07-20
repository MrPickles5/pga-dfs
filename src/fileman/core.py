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
            #'raw': None,
            'pkl': 'strokes-gained.pkl',
            'component': 'sg-{}.pkl' #.format()
        },
        
        'optimizer': {
            'raw': 'optimizer-raw.pkl',
            'clean': 'optimizer-clean.pkl'
        }
    }
    
    @classmethod
    def fanduel(param=None):
        return pkl_fs+paths['fanduel']['pkl'] if param is None else csv_fs+paths['fanduel']['csv']
    
    @classmethod
    def strokes_gained(param=None):
        return pkl_fs+paths['strokes']['pkl'] if component is None else pkl_fs+paths['strokes']['component'].format(shorten.get(param,param))
    
    @classmethod
    def optimizer(param=None):
        return pkl_fs+paths['optimizer'][f'{"clean" if param is None else "raw"}']
    
    @classmethod
    def getfs(ftype, fparam):
        
        if ftype == 'strokes' and fparam is not None:
            return strokes_gained(fparam)
        
        return { 'fanduel': fanduel(fparam), 'strokes-gained': strokes_gained(fparam), 'optimizer': strokes_gained(fparam) }.get(ftype, None)
    
