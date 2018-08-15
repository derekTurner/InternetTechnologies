from http.server import BaseHTTPRequestHandler, HTTPServer


class myHandler(BaseHTTPRequestHandler):
   def do_GET(self):
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()
      self.wfile.write(bytes("<h1>Hello World !</h1>", 'utf-8'))


server = HTTPServer(('', 8088), myHandler)
print('Started httpserver')
server.serve_forever()
