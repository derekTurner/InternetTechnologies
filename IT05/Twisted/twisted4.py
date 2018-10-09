from twisted.web.server import Site
from twisted.web.resource import Resource, NoResource
from twisted.internet import reactor, endpoints
from calendar import calendar


class YearPage(Resource):
    def __init__(self, year):
        Resource.__init__(self)
        self.year = year

    def render_GET(self, request):
        page = ("<html><body><pre>%s</pre></body></html>" %
                (calendar(self.year),))
        return page.encode('utf-8')


class CalendarHome(Resource):
    def getChild(self, name, request):
        if name == '':
            return self
        if name.isdigit():
            return YearPage(int(name))
        else:
            return NoResource()

    def render_GET(self, request):
        return b"<html><body>Welcome to the calendar server!</body></html>"


root = CalendarHome()
factory = Site(root)
endpoint = endpoints.TCP4ServerEndpoint(reactor, 8880)
endpoint.listen(factory)
reactor.run()

# https://twistedmatrix.com/documents/current/web/howto/web-in-60/dynamic-dispatch.html
