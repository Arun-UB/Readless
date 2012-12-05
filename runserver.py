from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from server import app
import os

if __name__ == '__main__':
    env = os.environ.get('ENV')
    if env == 'pro':
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(5000)
        IOLoop.instance().start()
    else:
        app.run()
