#!/usr/bin/env python3

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
import json


class JSONHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        raise NotImplementedError

    def do_POST(self):
        raise NotImplementedError

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
