from collections import OrderedDict

from FormGUI.Project.Meta import Meta
from FormGUI.SQLite.BasicFields import BasicFields

class Norm:
    ''' With the use of other data-conversion packages, the opportunities
    for data-normalization have expanded considerably. It's time to combine
    them so as to use / maintain each, in a common location.
    '''

    @staticmethod
    def BaseName(source):
        ''' Remove any path characters. '''
        for sep in Meta.SEPS:
            ipos = source.find(sep)
            if ipos is not -1:
                source = source.split(sep)[-1]
        return source

    @staticmethod
    def Remove(source, suffix):
        ''' Detect & remove (1) file suffix and (2) Path Names.'''
        source = Norm.BaseName(source)           
        if source.endswith(suffix):
            return source[0:-len(suffix)]
        return source

    @staticmethod
    def NormPath(path):
        ''' Convert a path to evaluatable path-name. '''
        if path:
            return path.replace('\\', '/')
        return path
    
    @staticmethod
    def NormLine(line, sep=','):
        ''' Normalize & split the first line / header line from a data-file. '''
        if ord(line[0]) == 65279:
            line = line[1:] # skip the UTF-16 BOM
        cols = line.split(sep)
        results = []
        for col in cols:
            col = col.replace('"', ' ').strip()
            results.append(col)
        return results        

    @staticmethod
    def NormCol(name):
        ''' Normalize an SQL column-name '''
        if not name:
            return ''
        if ord(name[0]) == 65279:
            name = eval(name[1:])
        name = str(name).strip()
        return BasicFields.MkGoodName(name)

    @staticmethod
    def NormCols(fields):
        ''' Fields are managed as an ordered dictionary. Uses NormCol(.)'''
        if not fields:
            return fields # gigo - (commonly used asa flag!)
        if isinstance(fields, list):
            zdict = OrderedDict()
            for field in fields:
                zdict[field[0]] = field[1]
            fields = zdict
        results = OrderedDict()
        bFirst = True
        for key in fields:
            key2 = Norm.NormCol(key)
            results[key2] = fields[key]
        return results
