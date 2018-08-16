from http.server import BaseHTTPRequestHandler, HTTPServer


class myHandler(BaseHTTPRequestHandler):
   def Send200(self, mess):
      try:
         self.send_response(200)
         self.send_header('Content-type', 'text/plain')
         self.end_headers()
         self.wfile.write(bytes(mess, 'utf-8'))
      except ConnectionResetError:
         pass

   def do_GET(self):
      pp = self.path.split('/')
      if len(pp) < 3:
         self.Send200(self.path +' is too short')
      elif pp[2] == 'Employee':
         self.Send200('Employee request')
      elif pp[2] == 'Post':
         self.Send200('Post request')
      elif pp[2] == 'Holiday':
         self.Send200('Holiday request')
      else:
         self.Send200("Hello World !")


server = HTTPServer(('', 8088), myHandler)
print('Started httpserver')
server.serve_forever()
