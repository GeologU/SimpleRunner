#!/usr/bin/env python3

from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import json
import random
import time
import datetime
import threading


class SmallHTTPRequestHandler(BaseHTTPRequestHandler):

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

    def return_content(self, status, content_type, content, headers=None):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(content))

        if headers is not None:
            for k, v in headers.items():
                self.send_header(k, v)
        self.end_headers()

        self.wfile.write(content)

    def return_json(self, status, obj):
        content = json.dumps(obj, indent=2, sort_keys=True).encode('UTF-8')
        return self.return_content(status, 'application/json', content)

    def show_bad_path(self):
        return self.return_json(HTTPStatus.NOT_FOUND, {
            'error': 'No path found on server: ' + self.path,
        })

    def show_exception(self, exc):
        return self.return_json(HTTPStatus.INTERNAL_SERVER_ERROR, {
            'error': 'Internal server error',
            'details': str(exc),
        })

    def read_data(self):
        data_size = self.headers['Content-Length']
        if data_size:
            return self.rfile.read(int(data_size))
        return None

    def read_json(self):
        data = self.read_data()
        if data is not None:
            return json.loads(data)
        return None

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


def run(server_class=ThreadingHTTPServer, handler_class=SmallHTTPRequestHandler):
    server_address = ('', 8001)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
