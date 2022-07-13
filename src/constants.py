import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

tournament = 'British Open'

focus_stat = 'putt-sg'
focus_stat_2 = 'arg-sg'

create = True
display_num = 10

keep_cols = [
    # 'Id',
    'Nickname',
    'FPPG',
    'Played',
    'Salary',
    'Injury Indicator'
]

def pandas_settings():
    pd.set_option("display.max_rows",1000)
    pd.set_option("display.max_columns",1000)
    pd.set_option("display.width", 1000)
    pd.set_option("display.memory_usage", False)
    pd.options.display.float_format = '{:.2f}'.format
    
    plt.rcParams["figure.figsize"] = [10, 10]
    plt.rcParams["lines.linewidth"] = 20
    plt.style.use('fivethirtyeight')
    
    return None

def tournament_fname():
    return(tournament.lower().replace(' ', '-'))



# tournament = 'Scottish Open'