"""JSON formatters etc"""
from datetime import datetime

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
   x = c.execute('select * from '+ tp +' where '+ cond)
   for r in x:
      ob = ob.__class__()
      GetOne(x, ob, r)
      sb += cm + Stringify(ob)
      cm = ','
   c.close()
   return sb + ']'

def Fill(ob,s):
    off = 1
    while off < len(s)-1:
        if s[off]=='}':
            return
        c = s.index(':',off)
        if s[off]=='"':
            f = s[off+1:c-1]
        else:
            f = s[off:c]
        off = c+2
        c = s.find(',',off)
        b = s.find('}',off)
        if c<0 or (b>0 and b<c):
            c = b
        v = getattr(ob,f)
        if isinstance(v,str):
            setattr(ob,f,s[off+1:c-1])
        elif isinstance(v,int):
            setattr(ob,f,int(s[off:c]))
        elif isinstance(v,float):
            setattr(ob,f,float(s[off:c]))
        elif isinstance(v,datetime):
            d = datetime.strptime(s[off+1:c-1],'%Y-%m-%d')
            setattr(ob,f,d)
        off = c
        if s[off]=='}':
            return
        off+= 2
    return

def PostSQL(ob):
    tp = ob.__class__.__name__
    sb = 'insert into '+tp+'('
    sc = ') values ('
    cm = ''
    for f in dir(ob):
        if f[0]!='_':
            v = getattr(ob,f)
            if v==None:
                continue
            sb += cm+f
            sc += cm
            cm = ','
            if isinstance(v,datetime):
                v = v.strftime('%Y-%m-%d')
            if isinstance(v,str):
                sc+="'"
            sc += str(v)
            if isinstance(v,str):
                sc+="'"
    return sb+sc+')'
