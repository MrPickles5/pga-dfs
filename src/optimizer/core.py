import numpy as np
import pandas as pd

import itertools
from itertools import combinations

from functools import cache
from tqdm.notebook import tqdm

from pandarallel import pandarallel
pandarallel.initialize(use_memory_fs=True)

import constants
import constraints

from datagolf import DataGolf
from fileman import fileman
from pga import PGA
from picklejar import PickleJar

from dataprep import DataPrep

constants.pandas_settings()

class Optimizer:
    
    data = DataPrep.OptimizedData()
    pnames = data.index.values.tolist()
    
    @classmethod
    @cache
    def get_value(cls, name, column):
        return( cls.data.loc[name, column] )
    
    @classmethod
    @cache
    def sum_values(cls, names, column):
        return( sum( [ cls.get_value(name, column) for name in names ] ) )
    
    @classmethod
    @cache
    def is_valid_lineup(cls, lineup):
        return( cls.sum_values(lineup, 'salary') in constraints.cost_range and len(set(lineup))==6 )
    
    @classmethod
    @cache
    def lineup_analysis(cls, lineup):
        return(tuple( [ cls.sum_values(tuple(set(lineup)),column) for column in constraints.cols_to_sum ] ) )
    
    @classmethod
    def lineup_analysis_wrapper(cls, lineup):
        return( cls.lineup_analysis(tuple(set(lineup.to_numpy()))) if cls.is_valid_lineup(tuple(set(lineup.to_numpy()))) else (0.0,)*len(constraints.cols_to_sum)  )
    
    @staticmethod
    def create_lineup_2_slices(slate_dict):
    #     2 things of three
        ret_list = list()

        for half_slates in tqdm( [p for p in itertools.product(*slate_dict.values())] ):
            g1,g2,g3 = tuple(sorted(list(half_slates[0])))
            g4,g5,g6 = tuple(sorted(list(half_slates[1])))

            lu = (g1,g2,g3,g4,g5,g6)
            if cls.is_valid_lineup(lu):
                ret_list.append(lu)

        return tuple(ret_list)
    
    @staticmethod
    def create_lineup_3_slices(slate_dict):
    #     3 things of two
        ret_list = list()

        for third_slates in tqdm( [p for p in itertools.product(*slate_dict.values())] ):
            g1,g2 = tuple(sorted(list(third_slates[0])))
            g3,g4 = tuple(sorted(list(third_slates[1])))
            g5,g6 = tuple(sorted(list(third_slates[2])))

            lu = (g1,g2,g3,g4,g5,g6)
            if cls.is_valid_lineup(lu):
                ret_list.append(lu)

        return tuple(ret_list)

    # Trying to get better about only passing tuples or other completely immutable for default and for cache
    @classmethod
    def Create(cls):

        # Not necessary but makes reading easier
        num_players = 6 # (n)
        num_slices = constraints.slices

        step = int( len(cls.pnames) * num_slices**-1 ) # Refers to partition of all names --> 2 slices of 120 players == (:120,120:)
        r = int(num_players / num_slices) # (nCr)

        slates = dict()
        if num_slices == 2:
            slates = {
                'slate1': tuple(map( tuple, itertools.combinations(cls.pnames[:step], r) )),
                'slate2': tuple(map( tuple, itertools.combinations(cls.pnames[step:], r) ))
            }

        elif num_slices == 3:
            slates = {
                'slate1': tuple(map( tuple, itertools.combinations(cls.pnames[:step], r) )),
                'slate2': tuple(map( tuple, itertools.combinations(cls.pnames[step:int(2*step)], r) )),
                'slate3': tuple(map( tuple, itertools.combinations(cls.pnames[int(2*step):], r) )),
            }

        lineups = cls.create_lineup_2_slices(slates) if num_slices==2 else cls.create_lineup_3_slices(slates)
        ret = pd.DataFrame(lineups, columns=['g1','g2','g3','g4','g5','g6'])

        # Badda bing
        ret[constraints.cols_to_sum] = ret.parallel_apply( lineup_analysis_wrapper, axis=1, result_type='expand' )
        ret = (ret
               .sort_values(by='proj-pts', ascending=False)
               .drop_duplicates()
               .reset_index(drop=True)
              )

        PickleJar.prepare(ret, 'created')
        print('Done...')

        return None
    
    @staticmethod
    def output_lineups_by(sort_by):
        return PickleJar.load('created').sort_values(by=sort_by[0], ascending=False).head(100)
    
    @classmethod
    def Run(cls, sort_by=('proj-pts',)):
        print('Creating lineups...\n')
        cls.Create()
        return output_lineups_by(sort_by)
    