import Json
from datetime import datetime


class HOLIDAY:
    """Python class representing a row of the HOLIDAY table"""

    def __init__(self):
        self.empid = 0
        self.hfrom = datetime(1900, 1, 1)
        self.hto = datetime(1900, 1, 1)
        self.agreed = datetime(1900, 1, 1)
        self.rvv = 0
        return

    @classmethod
    def _GetAllWith(HOLIDAY, id, conn):

        cond = "empid = " + str(id)
        h = HOLIDAY()
        return Json.GetAllWith(h, conn, cond)

    @classmethod
    def _FindNth(POST, id, n, conn):
        c = conn.cursor()
        x = c.execute('select * from POST where empid=' + str(id))
        h = HOLIDAY()
        if n > 1:
            for i in range(1, n):
                c.fetchone()
        text = Json.GetOne(x, h, c.fetchone())
        c.close()
        return text


class HOLIDAY1(HOLIDAY):
    def __init__(self):
        self.emp_rvv = 0
        self.post_rvv = 0
        super().__init__()
