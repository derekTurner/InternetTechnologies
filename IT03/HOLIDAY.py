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
    return  Json.GetAllWith(h, conn, cond)