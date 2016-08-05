#!/usr/bin/env python
import tornado.ioloop
import tornado.web
import tornado.template

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader("./templates")
        self.write(loader.load("home.html").generate(DEBUG=True)) # FIXME

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': './static' }),
    ], debug=True) # FIXME

if __name__ == "__main__":
    app = make_app()
    app.listen(8888) # FIXME Make this configurable
    tornado.ioloop.IOLoop.current().start()