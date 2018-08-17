import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from EMPLOYEE import *
from POST import POST
from HOLIDAY import HOLIDAY
import Json


class myHandler(BaseHTTPRequestHandler):
   def Send200(self, mess):

      try:
         self.send_response(200)
         self.send_header('Content-type', 'text/plain')
         self.end_headers()
         self.wfile.write(bytes(mess, 'utf-8'))
      except ConnectionResetError:
         pass

   def SendError(self, status, mess):

      try:
         self.send_response(status)
         self.send_header('Content-type', 'text/plain')
         self.end_headers()
         self.wfile.write(bytes(mess, 'utf-8'))
      except ConnectionResetError:
         pass

   def do_GET(self):

      pp = self.path.split('/')
      if len(pp) < 3:
         self.Send200(self.path + ' is too short')
      elif pp[2] == 'Employee':
        self.Send200(self.GetEmployee(pp))
      elif pp[2] == 'Post':
         self.Send200(self.GetPost(pp))
      elif pp[2] == 'Holiday':
         self.Send200(self.GetHoliday)
      else:
         self.SendError(400, 'Expected one of Employee/,Post/,Holiday/')

   def GetData(self):
      if not self.headers.__contains__('Content-Length'):
         return None
      h = self.headers.__getitem__('Content-Length')
      n = int(h)
      return str(self.rfile.read(n), 'utf-8')

   def do_POST(self):
      try:
         s = self.GetData()
         self.Send200(s + ' was posted')
      except Exception as e:
         self.SendError(500, repr(e))
      return

   def GetEmployee(self,p):
        if len(p)<4:
            return Json.GetAll(EMPLOYEE(),conn)
        id = int(p[3])
        return Json.Stringify(EMPLOYEE._Find(id,conn)) 

   def GetPost(self,p):
        if len(p)<4:
            return Json.GetAll(POST(),conn)
        id = int(p[3])
        return Json.Stringify(POST._GetAllWith(id,conn)) #

   def GetHoliday(self,p):
        if len(p)<4:
            return Json.GetAll(HOLIDAY(),conn)
        id = int(p[3])
        return Json.Stringify(HOLIDAY._GetAllWith(id,conn)) #


conn = sqlite3.connect('Payroll.db')
server = HTTPServer(('', 8088), myHandler)
print('Started httpserver')
server.serve_forever()
