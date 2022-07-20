import constants

slices=2
min_salary=8250
cost_range = range(595,601)

sg_cols = [ constants.focus_stat, constants.focus_stat_2, constants.focus_stat_3 ]
val_cols = [f'{constants.focus_stat}-per-10k', f'{constants.focus_stat_2}-per-10k', f'{constants.focus_stat_3}-per-10k']

if constants.focus_stat_2 is None:
    sg_cols = sg_cols[:1]
    val_cols = val_cols[:1]
    
elif constants.focus_stat_3 is None:
    sg_cols = sg_cols[:2]
    val_cols = val_cols[:2]

cols_to_sum = ['salary', 'proj-pts'] #, 'cfit-pts'] #+ sg_cols + val_cols
cols_order = [
    'salary',
    'proj-pts',
    #'cfit-pts',
    #constants.focus_stat,
    #f'{constants.focus_stat}-per-10k',
    #constants.focus_stat_2,
    #f'{constants.focus_stat_2}-per-10k',
    #constants.focus_stat_3,
    #f'{constants.focus_stat_3}-per-10k', 
]