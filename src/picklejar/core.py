import pandas as pd

from ..fileman import fileman


class PickleJar:
    
    @staticmethod
    def prepare(df, ftype, fparam=None):
        df.to_pickle( fileman.getfs(ftype,fparam) )
        return None
    
    @staticmethod
    def load(ftype, fparam=None):
        return pd.read_pickle(fileman.getfs(ftype, fparam))
    