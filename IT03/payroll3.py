from http.server import BaseHTTPRequestHandler, HTTPServer


class myHandler(BaseHTTPRequestHandler):
   def Send200(self, mess):
      self.send_response(200)
      self.send_header('Content-type', 'text/plain')
      self.end_headers()
      self.wfile.write(bytes(mess, 'utf-8'))

   def do_GET(self):
      self.Send200("<h1>Hello World</h1>!")


server = HTTPServer(('', 8088), myHandler)
print('Started httpserver')
server.serve_forever()
