import os
import pandas as pd

import constants

class fileman:
#     Class attributes
    
    root = os.getcwd().replace('src','data/')+'pickle-buffer/'
    
    shorten = {'tee': 'ott', 'approach': 'app', 'around': 'arg', 'green': 'putt', 'tee-to-green': 'ttg'}
    fnames = {
        'combined': 'combined.pkl',
        'created': f'{constants.tournament}.pkl',
        
        'datagolf': '{}.pkl',
        
        'fanduel': f'{constants.tournament}.pkl',
        'skills': 'skills-decomp.pkl',
        
        'strokes' : {
            'component': 'sg-{}.pkl',
            'aggregate': 'strokes-gained.pkl'
        },
        
        'optimizer': {
            'raw': 'optimizer-raw.pkl',
            'clean': 'optimizer-clean.pkl'
        }
    }
    
    # paths = { k: root+v for k,v in files.items() }
    @classmethod
    def combined(cls):
        return cls.root + cls.fnames['combined']
    
    @classmethod
    def created(cls):
        return cls.root.replace('pickle-buffer', 'lineups-created')+cls.fnames['created']
    
    @classmethod
    def datagolf(cls, fname):
        return cls.root.replace('pickle-buffer', 'datagolf-raw') + cls.fnames['datagolf'].format(fname)
    
    @classmethod
    def fanduel(cls, param=None):
        return cls.root + cls.fnames['fanduel'] if param is None else cls.root.replace('pickle-buffer', 'contest-files') + cls.fnames['fanduel'].replace('pkl', 'csv')
    
    @classmethod
    def skills(cls):
        return cls.root + cls.fnames['skills']
    
    @classmethod
    def strokes_gained(cls, param=None):
        return cls.root + cls.fnames['strokes']['aggregate'] if param is None else cls.root + cls.fnames['strokes']['component'].format(cls.shorten.get(param,param))
    
    @classmethod
    def optimizer(cls, param=None):
        return cls.root + cls.fnames['optimizer'][f'{"clean" if param is None else "raw"}']
    
    @classmethod
    def getfs(cls, ftype, fparam):
        
        ret_fs = {
            'combined': cls.combined(),
            'created': cls.created(),
            'datagolf': cls.datagolf(fparam),
            'fanduel': cls.fanduel(fparam),
            'skills': cls.skills(),
            'strokes': cls.strokes_gained(fparam),
            'optimizer': cls.optimizer(fparam)
        }
        
        return ret_fs.get(ftype, None)
    
