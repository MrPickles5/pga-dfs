import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

tournament = '3m-open' # Automate somehow?

focus_stat_1 = 'ttg-sg'
focus_stat_2 = 'app-sg'
focus_stat_3 = 'arg-sg'

def focus_stats():

    stats = [ focus_stat_1 ]
    if focus_stat_2 is not None:
        stats.append(focus_stat_2)
        if focus_stat_3 is not None:
            stats.append(focus_stat_3)

    return tuple(stats)


create = True
display_num = 10

fanduel_cols = [
    # 'Id',
    'Nickname',
    'FPPG',
    'Played',
    'Salary',
    'Injury Indicator'
]

# Customization / style file later
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

pandas_settings()