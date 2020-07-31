from collections import OrderedDict

class BasicFields(object):

    """
    Name implies that we are interested in basic, SQLite, data types?
    The ID field should always be present. Integral. Constraint is AUTO.
    Foreign-key relationships - if required - must be user-managed.
    User-defined field constraints, are not supported.
    """

    BADIES = ' ', '\n', '\r', '\t', '\\', '/', ':', ';'
    SupportedTypes = {
    "INTEGER":["INTEGER", "INT", "TINYINT", "SMALLINT", "MEDIUMINT", "BIGINT",
    "INT2", "INT4", "INT8"],
    "REAL":["REAL", "DOUBLE", "DOUBLE PRECISION", "FLOAT", "MONEY"],
    "TEXT":["TEXT", "STRING", "VARCHAR"],
    "BLOB":["BLOB", "BYTE[]"]
    }

    def __init__(self):
        self.fields = OrderedDict()
        self.fields["ID"] = "Integer"

    def add_field(self, zName, zType):
        if not BasicFields.IsGoodName(zType):
            return False
        if not BasicFields.IsType(zType):
            return False
        self.fields[zName] = zType.upper()
        return True

    def get_fields(self):
        return self.fields

    def has_fields(self):
        return len(self.fields) > 0

    @staticmethod
    def IsType(zType):
        return zType.upper() in BasicFields.SupportedTypes

    @staticmethod
    def MkGoodName(zName):
        ''' We could do a lot more here, covering the basics... '''
        if not zName:
            return ''
        for ch in BasicFields.BADIES:
            zName = zName.replace(ch, '_')
        return zName

    @staticmethod
    def IsGoodName(zName):
        ''' We could do a lot more here, covering the basics... '''
        for ch in BasicFields.BADIES:
            if zName.find(ch) != -1:
                return False
        return True



