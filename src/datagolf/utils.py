# Separate file for helper functions that can be applied throughout api file



def clean_name(name):
    if len(name.split(' '))==2:
        parts=name.replace(' ', '').split(',')
        return(' '.join([parts[1],parts[0]]))
    elif len(name.split(' '))==3:
        parts=name.replace(',', '').split(' ')
        return(' '.join([parts[1], parts[2], parts[0]]))
    
    return 'Issue'

