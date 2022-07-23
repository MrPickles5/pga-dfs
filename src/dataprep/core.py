import numpy as np
import pandas as pd

import constants
import constraints

from datagolf import DataGolf
from fileman import fileman
from pga import PGA
from picklejar import PickleJar

class DataPrep:
    
    @staticmethod
    def contest_data():
        df = PickleJar.load('fanduel', 'raw')
        ret = (df
               .rename({'nickname': 'name'}, axis=1)
               .loc[(df['injury indicator']!='O')]
               .drop('injury indicator', axis=1)
               .dropna()
               .reset_index(drop=True)
              )

        PickleJar.prepare(ret, 'fanduel')
        return None
    
    @classmethod
    def FanDuel(cls):
        cls.contest_data()
        return PickleJar.load('fanduel')
    
    @classmethod
    def combine_pga_fanduel(cls):
        
        fd = cls.FanDuel()
        sg = PGA.StrokesGained()
        
        focus_stats = constants.focus_stats()
        sg_lookup = PickleJar.load_set_idx('strokes', idx='name')
        for sg_col in focus_stats:
            fd[sg_col] = fd['name'].apply(lambda x: sg_lookup.loc[x, sg_col] if x in sg_lookup.index else 0.0)
            fd[f'{sg_col}-per-10k'] = np.array( 10000 * fd[sg_col] / fd['salary'] )

        combo = (fd
                 .dropna()
                 .reset_index(drop=True)
                )

        PickleJar.prepare(combo, 'combined')

        return None
    
    @classmethod
    def synthesize(cls):
        cls.combine_pga_fanduel()
        return PickleJar.load('combined')
    
    @classmethod
    def add_constraints(cls):
    
        ret = cls.synthesize()

        if constraints.min_salary is not None:
            print(f'Excluding players less than ${constraints.min_salary}...')
            ret = (ret
                   .loc[ ret['salary']>=constraints.min_salary ]
                   .reset_index(drop=True)
                  )

        PickleJar.prepare(ret, 'optimizer', fparam='raw')
        return None
    
    @classmethod
    def add_datagolf(cls):
        
        cls.add_constraints()
        ret = PickleJar.load('optimizer', fparam='raw')
        
        projections = DataGolf.dfs()
        probabilities = DataGolf.baselines() 

        projections.index = projections['name']
        probabilities.index = probabilities['name']

        ret['proj-pts'] = ret['name'].apply(lambda x: projections.loc[x,'points'] if x in ret.index else 0.0)
        ret['proj-own'] = ret['name'].apply(lambda x: projections.loc[x,'ownership'] if x in ret.index else 0.0)

        ret['make-cut'] = ret['name'].apply(lambda x: probabilities.loc[x,'make-cut'] if x in ret.index else 0.0)
        ret['top-10'] = ret['name'].apply(lambda x: probabilities.loc[x,'top-10(%)'] if x in ret.index else 0.0)

        ret['salary'] /= 100

        PickleJar.prepare(ret, 'optimizer')
        
        return None
    
    @classmethod
    def OptimizedData(cls):
        cls.add_datagolf()
        return PickleJar.load_set_idx('optimizer', idx='name')
    