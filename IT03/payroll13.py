import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from EMPLOYEE import *
from POST import POST, POST1
from HOLIDAY import HOLIDAY, HOLIDAY1
import Json
import base64


class myHandler(BaseHTTPRequestHandler):

    validNames = ('Employee', 'Post', 'Holiday')

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
            if status == 401:
                self.send_header('WWW-Authenticate', 'Basic realm="Payroll"')
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes(mess, 'utf-8'))
        except ConnectionResetError:
            pass

    def do_GET(self):
        valid = False
        errorMessage = ''
        try:
            self.Authenticate()
        except Json.RestException as e:
            self.SendError(e.error, e.args[0])
        except Exception as e:
            self.SendError(403, repr(e))
        else:
            pp = self.path.split('/')
            if len(pp) < 3:
                valid = False
                errorMessage = self.path + ' is too short'
            if len(pp) > 2:
                valid = pp[2] in self.validNames
                if not valid:
                    errorMessage = 'Expected one of'
                    for self.validName in self.validNames:
                        errorMessage += '/' + self.validName + ', '
            if (valid and len(pp) > 3):
                valid = pp[3].isnumeric()
                if valid:
                    valid = (int(pp[3]) > 0)
                if not valid:
                    errorMessage = 'Invalid identifier'
            if (valid and len(pp) == 5):
                valid = pp[4].isnumeric()
                if valid:
                    valid = (int(pp[4]) > 0)
                if not valid:
                    errorMessage = 'Invalid index'

            if not valid:
                self.SendError(400, errorMessage)
            else:
                if pp[2] == 'Employee':
                    self.Send200(self.GetEmployee(pp))
                if pp[2] == 'Post':
                    self.Send200(self.GetPost(pp))
                if pp[2] == 'Holiday':
                    self.Send200(self.GetHoliday(pp))

    def GetData(self):
        if not self.headers.__contains__('Content-Length'):
            return None
        h = self.headers.__getitem__('Content-Length')
        n = int(h)
        return str(self.rfile.read(n), 'utf-8')

    def do_POST(self):
        try:
            self.Authenticate()
        except Json.RestException as e:
            self.SendError(e.error, e.args[0])
        except Exception as e:
            self.SendError(403, repr(e))
        else:
            try:
                s = self.GetData()
                p = self.path.split('/')
                if len(p) >= 3:
                    if p[2] == 'Employee':
                        self.Send200(self.PostEmployee(s))
                        return
                    elif p[2] == 'Post':
                        self.Send200(self.PostPost(s))
                        return
                    elif p[2] == 'Holiday':
                        self.Send200(self.PostHoliday(s))
                        return
                self.SendError(400, 'Expected one of Employee/,Post/,Holiday/')
            except Exception as e:
                self.SendError(500, repr(e))
            return

    def do_PUT(self):
        try:
            self.Authenticate()
        except Json.RestException as e:
            self.SendError(e.error, e.args[0])
        except Exception as e:
            self.SendError(403, repr(e))
        else:
            try:
                s = self.GetData()
                p = self.path.split('/')
                if len(p) >= 3:
                    if p[2] == 'Holiday':
                        self.Send200(self.PutHoliday(s))
                        return
                self.SendError(400, 'Expected one of Employee/,Post/,Holiday/')
            except Exception as e:
                self.SendError(500, repr(e))
            return

    def GetEmployee(self, p):
        if len(p) < 4:
            return Json.GetAll(EMPLOYEE(), conn)
        id = int(p[3])
        return Json.Stringify(EMPLOYEE._Find(id, conn))

    def GetPost(self, p):
        if (len(p) == 5):
            return (POST._FindNth(int(p[3]), int(p[4]), conn))
        elif (len(p) == 4):
            return (POST._GetAllWith(int(p[3]), conn))
        elif (len(p) == 3):
            return Json.GetAll(POST(), conn)

    def GetHoliday(self, p):
        if (len(p) == 5):
            return (HOLIDAY._FindNth(int(p[3]), int(p[4]), conn))
        elif (len(p) == 4):
            return (HOLIDAY._GetAllWith(int(p[3]), conn))
        elif (len(p) == 3):
            return Json.GetAll(HOLIDAY(), conn)

    def GetRvv(self):
        c = conn.cursor()
        c.execute('update rvv set seq=seq+1')
        c.close()
        c = conn.cursor()
        rn = int(c.execute('select seq from rvv').fetchone()[0])
        c.close()
        return rn

    def PostEmployee(self, s):
        e = EMPLOYEE()
        Json.Fill(e, s)
        e.rvv = self.GetRvv()
        conn.execute(Json.PostSQL(e))
        conn.commit()
        return 'OK'

    def PostPost(self, s):
        p1 = POST1()
        Json.Fill(p1, s)
        Json.CheckRvv(EMPLOYEE(), p1.emp_rvv, conn)
        p = POST()
        p.empid = p1.empid
        p.efrom = p1.efrom
        p.grade = p1.grade
        p.manager = p1.manager
        p.rvv = self.GetRvv()
        conn.execute(Json.PostSQL(p))
        conn.commit()
        return 'OK'

    def PostHoliday(self, s):
        h1 = HOLIDAY1()
        Json.Fill(h1, s)
        Json.CheckRvv(EMPLOYEE(), h1.emp_rvv, conn)
        Json.CheckRvv(POST(), h1.post_rvv, conn)
        h = HOLIDAY()
        h.empid = h1.empid
        h.hfrom = h1.hfrom
        h.hto = h1.hto
        h.rvv = self.GetRvv()
        conn.execute(Json.PostSQL(h))
        conn.commit()
        return 'OK'

    def PutHoliday(self, s):
        h1 = HOLIDAY1()
        Json.Fill(h1, s)
        Json.CheckRvv(EMPLOYEE(), h1.emp_rvv, conn)
        Json.CheckRvv(POST(), h1.post_rvv, conn)
        oldrvv = h1.rvv
        h = HOLIDAY()
        h.agreed = h1.agreed
        h.empid = h1.empid
        h.hfrom = h1.hfrom
        h.hto = h1.hto
        h.rvv = self.GetRvv()
        conn.execute(Json.PutSQL(h, oldrvv))
        conn.commit()
        return

    def Authenticate(self):
        if not 'Authorization' in self.headers:
            raise Json.RestException(401, 'No authorization header')
        h = self.headers['Authorization']
        d = str(base64.b64decode(h[6:len(h)]), 'utf-8')
        s = d.split(':')
        c = conn.cursor()
        r = c.execute("select count(*) from user where uname='" +
                      s[0] + "' and password='" + s[1] + "'").fetchone()
        if int(r[0]) != 1:
            raise Json.RestException(401, 'Not authenticated')
        return


conn = sqlite3.connect('Payroll.db')
server = HTTPServer(('', 8088), myHandler)
print('Started httpserver')
server.serve_forever()
