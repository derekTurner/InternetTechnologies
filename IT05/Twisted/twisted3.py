from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor, endpoints
from twisted.web.static import File

root = Resource()
root.putChild(b"foo", File("./tmp"))  # add ./ to serve root of site
root.putChild(b"bar", File("./lost+found"))
root.putChild(b"baz", File("./opt"))

factory = Site(root)
endpoint = endpoints.TCP4ServerEndpoint(reactor, 8880)
endpoint.listen(factory)
reactor.run()

# https://twistedmatrix.com/documents/current/web/howto/web-in-60/static-dispatch.html
