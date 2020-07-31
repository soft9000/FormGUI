#!/usr/bin/env python3

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from collections import OrderedDict

from FormGUI.SQLite.BasicFields import BasicFields
from FormGUI.Project.Meta import Meta

class BasicTable(BasicFields):

    def __init__(self, name = Meta.DEFAULT_TABLE):
        super().__init__()
        self.table_name = BasicFields.MkGoodName(name);

    def get_table_name(self):
        return self.table_name

    @staticmethod
    def FromSQL(sql_create):
        """ Create a BasicTable from an SQL `CREATE` Statement. 
        Returns None if no SQL, False if unsupported SQL, else BasicTable.
        """
        sql_create = sql_create.replace('\r', '\n').replace('\n', ' ').replace('  ', ' ')
        zSplit = sql_create.split('(')
        if len(zSplit) is not 2:
            return None
        result = BasicTable(zSplit[0].split()[-1])
        zFields = zSplit[1].split(',')
        for field in zFields:
            if field.find('ID ') == 0:
                if not field.find('AUTO'):
                    return False # 80:20
                else:
                    continue     # We'll provide
            zName = field.split()[0]
            field = field.upper()
            for zKey in BasicFields.SupportedTypes:
                if field.startswith("VARCHAR"):
                    if(result.add_field(zName, "TEXT")):
                        continue
                if field in BasicFields.SupportedTypes[zKey]:
                    if(result.add_field(zName, zKey)):
                        continue
                    else:
                        return False # 98:02?
        if not result.has_fields():
            return None
        return result

    @staticmethod
    def Clone(basic_table):
        if not isinstance(basic_table, BasicTable):
            return None
        results = BasicTable(basic_table.table_name)
        results.fields = OrderedDict(basic_table.fields)
        return results






