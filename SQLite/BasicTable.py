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
    def Clone(basic_table):
        if not isinstance(basic_table, BasicTable):
            return None
        results = BasicTable(basic_table.table_name)
        results.fields = OrderedDict(basic_table.fields)
        return results






