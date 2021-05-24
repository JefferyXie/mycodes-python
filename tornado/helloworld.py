# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8888, help='run on the given port', type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world")

def main():
    tornado.options.parse_command_line()
    app = tornado.web.Application([(r"/", MainHandler)])
    svr = tornado.httpserver.HTTPServer(app)
    svr.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
