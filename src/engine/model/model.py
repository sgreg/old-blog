
class ModelObject(object):
    db_table = ""
    dbmap = []
    fields = dict()

    def __init__(self, resultset=None):
        self.fields = dict()
        if not self.mapResultset(resultset, self.fields, self.dbmap):
            raise AssertionError("Table values and fieldmap values mismatch: given %d needed %d  resultset %s" % (len(self.dbmap), len(resultset), str(resultset)))


    def mapResultset(self, resultset, fields, fieldmap):
        if 'id' not in fieldmap:
            fieldmap = ['id'] + fieldmap

        if resultset is None:
            for key in fieldmap:
                fields[key] = ""
            return True

        if len(resultset) != len(fieldmap):
            return False

        for i in range(len(resultset)):
            if resultset[i] is not None:
                fields[fieldmap[i]] = resultset[i]
            else:
                fields[fieldmap[i]] = ""

        return True


    def insertDbEntry(self, db):
        fmt = 'insert into ' + self.db_table + '(' + ', '.join(self.dbmap) + ') values(' + ', '.join(["%s" for x in self.dbmap]) + ')'
        args = tuple(self.fields[k] for k in self.dbmap)
        return db.execute(fmt, args)

    def updateDbEntry(self, db):
        fmt = 'update ' + self.db_table + ' set ' + ', '.join(["%s=%%s" % (key) for key in self.dbmap]) + ' where id=%s'
        args = (tuple(self.fields[k] for k in self.dbmap) + (self.fields['id'], ))
        return db.execute(fmt, args)

