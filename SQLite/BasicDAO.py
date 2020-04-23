#!/usr/bin/env python3

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from FormGUI.SQLite.BasicFields import BasicFields
from FormGUI.Project.Meta import Meta
from collections import OrderedDict

import sqlite3

class BasicDAO:
    """ 
    Class name implies that we are interested in a basic, "type 1," Table?
    Specifically:
        Classic 'ID' AUTO paradigm for the primary key is implied
        No constraints outside of the primary key
        No tech-mantained entity relationships
    """

    def __init__(self, file_name=Meta.DEFAULT_FILE_NAME):
        self.file = file_name
        self.conn = None
        self.curs = None
        self.bOpen = False
        self.fields = None
        self.table_name = None
        
    def _flat_keys(self, iter):
        result = None
        for ref in iter:
            if not result:
                result = "(" + str(ref)
            else:
                result += "," + str(ref)
        result += ")"
        return result

    def _flat_values(self, values):
        results = None
        for key in values:
            if not results:
                results = "("
            else:
                results += ","
            if self.fields[key] == "TEXT":
                results += "'" + values[key] + "'"
            else:
                results += str(values[key])
        results += ')'
        return results

    def exists(self):
        return os.path.exists(self.file)

    def delete_file(self):
        try:
            os.unlink(self.file)
            return True
        except:
            return False

    def is_defined(self):
        if not self.fields:
            return False
        if not self.table_name:
            return False
        return True

    def define(self, sql_fields, table_name='MyTable'):
        if not isinstance(sql_fields, BasicFields):
            return False
        if not BasicFields.IsGoodName(table_name):
            return False
        self.fields = sql_fields.get_fields();
        self.table_name = table_name
        return True

    def undefine(self):
        self.fields = self.table_name = None
        
    def open(self, bHasTable=True):
        """ 
        Open the database file. Default is to check for class field 
        associations. Use False for `query only` usage.
        
        Returns True upon success, else False.
        """
        if(bHasTable):
            if not self.is_defined():
                return False
        if self.bOpen is False:
            self.conn = sqlite3.connect(self.file)
            self.curs = self.conn.cursor()
            self.bOpen = True
        return True
        
    def close(self):
        if self.bOpen:
            self.conn.commit()
            self.bOpen = False
        return True
        
    def count(self):
        if self.bOpen:
            res = self.curs.execute(f"SELECT count(*) FROM {self.table_name};")
            return res.fetchone()[0]
        return -1
        
    def drop_table(self):
        if self.bOpen:
            self.curs.execute(f"DrOp TaBLe IF EXISTS {self.table_name};")
            return True
        return False
        
    def create_table(self):
        if self.bOpen:
            zStr = "ID INTEGER PRIMARY KEY AUTOINCREMENT"
            for field in self.fields:
                if field == 'ID':
                    continue
                zStr += ", "
                zStr += field + " " + self.fields[field]
            self.curs.execute(
                f"CREATE TABLE IF NOT EXISTS {self.table_name} ({zStr});")
            return True
        return False
        
    def insert(self, sql_fields):
         if self.bOpen:
            if not isinstance(sql_fields, dict):
                return
            for zKey in sql_fields:
                if zKey not in self.fields:
                    return
            zKeys   = self._flat_keys(sql_fields.keys())
            zValues = self._flat_values(sql_fields)
            return self.curs.execute(
                f"INSERT INTO {self.table_name} {zKeys} VALUES {zValues};").lastrowid
        
    def update(self, id_, sql_fields):
        if self.bOpen:
            if not isinstance(sql_fields, dict):
                return False
            for zKey in sql_fields:
                if zKey not in self.fields:
                    return False
            zSet = "SET "; bFirst = True
            for key in sql_fields:
                if not bFirst:
                    zSet += ", "
                else:
                    bFirst = False
                zValue = sql_fields[key]
                if isinstance(zValue, str):
                    zSet += key + f'="{zValue}"'
                else:
                    zSet += key + f"={zValue}"
            self.curs.execute(
                f"UPDATE {self.table_name} {zSet} WHERE ID = {id_};")
            return True
        return False
        
    def delete(self, primary_key):
        if self.bOpen:
            self.curs.execute(f"DELETE from {self.table_name} WHERE ID = ?;", [primary_key])
            return True
        return False
        
    def select(self, sql_select):
        if self.bOpen:
            self.curs.execute(sql_select)
            zlist = self.curs.fetchall()
            for ref in zlist:
                yield ref
        return None

if __name__ == '__main__':
    fields = BasicFields()
    assert(fields.add_field("Name", "TEXT"))
    assert(fields.add_field("Age", "INTEGER"))
    dao = BasicDAO()
    dao.delete_file()
    assert(dao.define(fields))
    assert(dao.open())
    assert(dao.create_table())
    assert(dao.insert({"Name":"John", "Age":21}))
    assert(dao.update(1, {"Age":22}))
    assert(dao.update(1, {"Name":"Jasper"}))
    assert(dao.insert({"Name":"Nagy", "Age":432}))
    assert(dao.count() == 2)
    for row in dao.select(f"select * from {dao.table_name};"):
        print(*row)
    dao.close()
    from FormGUI.Project.ProjectFile import ProjectFile
    for table in ProjectFile.Import(dao.file):
        for field in table.fields:
            print(table.table_name, field, table.fields[field])



        
    


