#!/usr/bin/env python3

from http import HTTPStatus
from http.server import HTTPServer
from socketserver import ThreadingMixIn
import random
import time
import datetime
import threading

from skeleton_json import SmallHTTPRequestHandler


class ExampleHanler(SmallHTTPRequestHandler):

    def do_GET(self):
        self.do_POST()

    def do_POST(self):
        try:
            if self.path == '/':
                self.show_index()
            elif self.path == '/sleep':
                self.show_sleep()
            else:
                self.show_bad_path()
        except Exception as exc:
            self.show_exception(exc)

    def show_index(self):
        return self.return_json(HTTPStatus.OK, {
            'index': '/',
            'sleeper': '/sleep',
        })

    def show_sleep(self):
        to_sleep = 2.5 + random.random()
        self.log_message('sleep: %.2f\tstarted at: %s', to_sleep, datetime.datetime.now())
        time.sleep(to_sleep)
        self.log_message('sleep: %.2f\tfinished at: %s', to_sleep, datetime.datetime.now())
        return self.return_json(HTTPStatus.OK, {
            'slept': to_sleep,
            'units': 'seconds',
            'thread': threading.get_ident(),
        })


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass


def run(server_class=ThreadingHTTPServer, handler_class=ExampleHanler):
    server_address = ('', 8001)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
