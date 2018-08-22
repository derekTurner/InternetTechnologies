import Json
from datetime import datetime


class POST:
    """Python class representing a row of the POST table"""

    def __init__(self):
        self.empid = 0
        self.efrom = datetime(1900, 1, 1)
        self.grade = ''
        self.manager = 0
        self.rvv = 0
        return

    @classmethod
    def _GetAllWith(POST, id, conn):

        cond = "empid = " + str(id)
        p = POST()
        return Json.GetAllWith(p, conn, cond)

    @classmethod
    def _FindNth(POST, id, n, conn):
        c = conn.cursor()
        x = c.execute('select * from POST where empid=' + str(id))
        p = POST()
        if n > 1:
            for i in range(1, n):
                c.fetchone()
        text = Json.GetOne(x, p, c.fetchone())
        c.close()
        return text


class POST1(POST):
    def __init__(self):
        self.emp_rvv = 0
        return super().__init__()
