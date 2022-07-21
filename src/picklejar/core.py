import pandas as pd

from fileman import fileman


class PickleJar:
    
    @staticmethod
    def prepare(df, ftype, fparam=None):
        df.to_pickle(fileman.getfs(ftype,fparam))
        return None
    
    @staticmethod
    def load(ftype, fparam=None):
        return pd.read_pickle( fileman.getfs(ftype, fparam) )
    
    @staticmethod
    def load_set_idx(ftype, fparam=None, idx=None):
        ret = pd.read_pickle(fileman.getfs(ftype, fparam))
        if idx is None or idx not in ret.columns:
            print( 'Please enter valid column to set as index (succesfully loaded, but no index was set)...\n' )
        
        else:
            ret.index = ret[idx]
            ret = ret.drop(idx, axis=1)
        
        return ret
            
            
    