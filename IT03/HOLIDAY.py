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
      c = conn.cursor()
    #  x = c.execute('select * from HOLIDAY where id='+str(id))
      e = HOLIDAY()
      Json.GetAllWith(e, conn, id)
      c.close()
      return e