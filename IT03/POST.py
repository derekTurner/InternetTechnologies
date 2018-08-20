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

        cond = "empid = " + str(id)
        p = POST()
        return  Json.GetAllWith(p, conn, cond)
        