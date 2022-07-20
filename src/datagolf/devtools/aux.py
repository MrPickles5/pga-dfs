# Separate file for helper functions that can be applied throughout api file

import numpy as np
import pandas as pd


class Clean:
    @staticmethod
    def name(name):
        return {
            2: ' '.join(name.replace(' ', '').split(',').reverse()),
            3: ' '.join(parts[1:]+[parts[0]])
        }.get(len(name.split(' ')), name)

        
    @staticmethod
    def names(pinfo_list):
        # for player in pinfo:
        #     player['player_name'] = name(player['player_name'])
        def conv(d):
            return {k: name(v) if k == 'player_name' else v for k, v in d.items()}
        
        return tuple([ conv(pinfo) for pinfo in pinfo_list ])
            
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