import os

from collections import OrderedDict

from FormGUI.SQLite.BasicDAO import BasicDAO
from FormGUI.SQLite.BasicTable import BasicTable
from FormGUI.Project.Normalizers import Norm
from FormGUI.Project.Meta import Meta

class ProjectFile(object):
   
    def __init__(self, name = Meta.DEFAULT_TABLE):
        self.project_tables = OrderedDict()
        self.project_name = name + Meta.ProjType

    def add_table(self, table):
        if not isinstance(table, BasicTable):
            return False
        self.project_tables[table.get_table_name()] = BasicTable.Clone(table)
        return True

    def fixup(self):
        # https://github.com/soft9000/PyDAO/blob/master/SqltDAO/SchemaDef/OrderDef.py
        ''' Enforce our "no file type" and "no file path" policies.
        '''
        self.project_name = Norm.Remove(self.project_name, Meta.ProjType)

    @staticmethod
    def Import(sql_file):
        dao = BasicDAO(sql_file)
        if not dao.exists():
            return None
        if not dao.open(False):
            return None
        results = list()
        for row in dao.select("SELECT * FROM sqlite_master WHERE name NOT LIKE 'sqlite_%';"):
            sql = row[-1]
            print(sql)
            zTable = BasicTable.FromSQL(sql)
            if zTable:
                results.append(zTable)
        return results

    @staticmethod
    def Fixup(project_file):
        ''' Returns False if the project_file cannot be fixed, else True. '''
        if not isinstance(project_file, ProjectFile):
            return False
        project_file.fixup()
        return True

    @staticmethod
    def LoadFile(fq_file):
        ''' Will return an Instance, else None
        '''
        results = ProjectFile()
        if not os.path.exists(fq_file):
            return None
        try:
            with open(fq_file, 'r') as fh:
                data = fh.read()
                zProj = eval(data)
                results.project_name = zProj["ProjectName"]
                zTables = eval(zProj["BasicTables"])
                for sub in zTables:
                    basic_table        = BasicTable(sub)
                    basic_table.fields =  zTables[sub]
                    results.add_table(basic_table)
                return results
        except Exception as ex:
            print(ex.__traceback__)
            return None

    @staticmethod
    def SaveFile(folder, project_file, overwrite=False):
        ''' Will always STORE an instance into the file name, if accessable.
        Default file-type extension. True / False returned.
        '''
        if not ProjectFile.Fixup(project_file):
            return False
        fq_file = folder + os.path.sep + project_file.project_name
        if not fq_file.endswith(Meta.ProjType):
            fq_file = fq_file + Meta.ProjType
        bExists = os.path.exists(fq_file)
        if bExists and overwrite is False:
            return False
        try:
            if bExists:
                os.unlink(fq_file)
            with open(fq_file, 'w') as fh:
                zOut = OrderedDict()
                zOut["Project"] = Meta.PRODUCT
                zOut["Version"] = Meta.VERSION
                zOut["ProjectName"] = project_file.project_name
                zDict = {}
                for table in project_file.project_tables:
                    sub = project_file.project_tables[table]
                    zDict[sub.table_name] = sub.fields
                zOut["BasicTables"] = repr(zDict)
                zformat = repr(zOut)
                print(str(zformat), file=fh)

            return os.path.exists(fq_file)
        except Exception as ex:
            print(ex)
            return False



