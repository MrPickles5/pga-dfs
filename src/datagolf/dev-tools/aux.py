# Separate file for helper functions that can be applied throughout api file

class Clean:
    @staticmethod
    def names(name):
        nparts = len(name.split(' '))
        if nparts == 2:
            parts = name.replace(' ', '').split(',').reverse()
            return ' '.join(parts)
        elif nparts == 3:
            parts = name.replace(',', '').split(' ')
            return ' '.join(parts[1:]+parts[0])
            
    @staticmethod
    def coltype(col):
        return {'name': 'str'}.get(col, 'float32')