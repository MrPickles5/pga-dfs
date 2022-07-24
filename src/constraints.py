import constants

slices=2
min_salary=9000
cost_range = range(593,601)

sg_cols = constants.focus_stats()
val_cols =  tuple(map(lambda x: f'{x}-per-10k', sg_cols))

cols_to_sum = ('salary', 'proj-pts', 'proj-own', 'make-cut', 'top-10')
cols_order = cols_to_sum + sg_cols + val_cols