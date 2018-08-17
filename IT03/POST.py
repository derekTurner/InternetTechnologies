import Json
from datetime import datetime

class POST:
    """Python class representing a row of the POST table"""
    def __init__(self):
        self.empid = 0
        self.efrom = datetime(1900,1,1)
        self.grade = ''
        self.manager = 0
        self.rvv = 0
        return

    @classmethod
    def _GetAllWith(POST, id, conn):
    #    def GetAllWith(ob, conn, cond):
    #    Json.GetOne(x,e,c.fetchone())
        c = conn.cursor()
    #    x = c.execute('select * from POST where id='+str(id))
        cond = "Empid = " + str(id)
        e = POST()
        Json.GetAllWith(e, conn, cond)
        c.close()
        return e