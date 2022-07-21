# Separate file for helper functions that can be applied throughout api file

import numpy as np
import pandas as pd


class Clean:
    @classmethod
    def name(cls, player):
        parts = player.split(' ') if len(player)==3 else player.replace(' ', '').split(',')
        formatting = { 2: ' '.join([parts[1], parts[0]]), 3: ' '.join(parts[1:]+[parts[0]]) }
        return formatting.get(len(player.split(' ')), player)

    @classmethod
    def polish(cls, d):
        return {k: cls.name(v) if k == 'player_name' else v for k, v in d.items()}


    @classmethod
    def names(cls, player_list):
        return tuple([ cls.polish(player) for player in player_list ])
            
    @staticmethod
    def columns(df):
        for col in df.columns:
            df[col]=df[col].astype({'name': 'str'}.get(col, 'float32'))
        return df
    
    
    
        # if nparts == 2:
        #     parts = 
        #     return ' '.join(parts)
        # elif nparts == 3:
        #     parts = name.replace(',', '').split(' ')
        #     return ' '.join(parts[1:]+[parts[0]])