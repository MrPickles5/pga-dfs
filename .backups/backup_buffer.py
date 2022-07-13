# When quickly changing functions to explore different results, faster to just copy and paste here then use git...
# That being said, use git when it gets beyond basic...

data = combine_with_fanduel().head(50)
data['salary'] /= 100

cols_to_sum = ['salary', constants.focus_stat, f'{constants.focus_stat}-per-10k']
cost_range = range(595,601)

@cache
def get_value(name, column):
    return( data.loc[name, column] )

@cache
def sum_values(names, column):
    return( sum( [ get_value(name, column) for name in names ] ) )

@cache
def is_valid_lineup(lineup):
    return( sum_values(lineup, 'salary') in cost_range )

@cache
def lineup_analysis(lineup):
    return(tuple( [ sum_values(tuple(set(lineup)),column) for column in cols_to_sum ] ) )

def lineup_analysis_wrapper(lineup):
    return( lineup_analysis(tuple(set(lineup.to_numpy()))) if is_valid_lineup(tuple(set(lineup.to_numpy()))) else (0.0,)*len(cols_to_sum)  )


def create_lineups():
    
    slates = tuple(map( tuple, itertools.combinations( data.index, 6 ) ))
    
    ret = pd.DataFrame(slates, columns=['g1','g2','g3','g4','g5','g6'])
    
    ret[cols_to_sum] = ret.parallel_apply( lineup_analysis_wrapper, axis=1, result_type='expand' )
    
    ret = ret.sort_values(by=f'{constants.focus_stat}-per-10k', ascending=False)
    
    ret.to_csv(f'../data/lineups-created/{constants.tournament_fname()}.csv', index=False)
    
    print('Done...')
    
    return None

def output_lineups(top_num=100):
    return(pd.read_csv(f'../data/lineups-created/{constants.tournament_fname()}.csv').head(top_num))
    