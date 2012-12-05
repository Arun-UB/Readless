from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from server import app
import os

if __name__ == '__main__':
    env = os.environ.get('ENV')
    if env == 'pro':
        http_server = HTTPServer(WSGIContainer(app))
        # Bind to PORT if defined, otherwise default to 5000.
        port = int(os.environ.get('PORT', 5000))
        http_server.listen(port)
        IOLoop.instance().start()
    else:
        app.run()
