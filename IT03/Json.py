# from types import *  is this line needed yet?

"""JSON formatters etc"""


def Stringify(ob):
   if ob == None:
      return '<null>'
   sb = '{'
   cm = ''
   for f in dir(ob):
      if f[0] != '_':
         v = getattr(ob, f)
         sb += cm + '"' + f + '": '
         cm = ', '
         if isinstance(v, str):
            sb += '"'
         sb += str(v)
         if isinstance(v, str):
            sb += '"'
   return sb + '}'


def GetOne(x, ob, r):
   if r == None:
      return ''
      #   d = dir(r)       is this line needed?
   for i in range(len(r)):
      f = x.description[i][0]
      setattr(ob, f, r[i])
   return Stringify(ob)


def GetAll(ob, conn):
   sb = '['
   cm = ''
   tp = ob.__class__.__name__
   c = conn.cursor()
   x = c.execute('select * from '+tp)
   for r in x:
      ob = ob.__class__()
      GetOne(x, ob, r)
      sb += cm + Stringify(ob)
      cm = ','
   c.close()
   return sb+']'


def GetAllWith(ob, conn, cond):
   tp = ob.__class__.__name__
   sb = '['
   cm = ''
   c = conn.cursor()
   x = c.execute('select * from '+tp+' where '+cond)
   for r in x:
      ob = ob.__class__()
      GetOne(x, ob, r)
      sb += cm + Stringify(ob)
      cm = ','
   c.close()
   return sb + ']'
