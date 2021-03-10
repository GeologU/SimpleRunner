#!/usr/bin/env python3

from html import escape
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import subprocess

import with_html_stack


class SmallHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.do_POST()

    def do_POST(self):
        if self.path == '/':
            self.show_index()
        elif self.path == '/command/':
            self.show_commands()
        elif self.path == '/schema/':
            self.show_schema()
        else:
            self.show_bad_path()

    def show_index(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'text/html')

        doc = with_html_stack.HTMLDocument()
        with doc('html', lang='en'):
            with doc('head'):
                doc('title', 'Select your task')
                doc('meta', _http_equiv='Content-type', content='text/html; charset=utf-8')
            with doc('body'):
                with doc('p'):
                    doc('a', 'View commands', href='/command/')
                with doc('p'):
                    doc('a', 'View dependencies of commands', href='/schema/')
        content = doc.content(with_html_stack.DEV_PARAMS)

        self.send_header('Content-Length', int(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def show_commands(self):
        commands = []
        output = subprocess.check_output(['./skeleton.sh', 'usage']).decode()
        for item in output.splitlines():
            x = item.split(maxsplit=1)
            if len(x) == 2:
                commands.append(x)

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'text/html')

        doc = with_html_stack.HTMLDocument()
        with doc('html', lang='en'):
            with doc('head'):
                doc('title', 'Select your task')
                doc('meta', _http_equiv='Content-type', content='text/html; charset=utf-8')
                with doc('style'):
                    doc.raw('table, td {border: 1px solid gray; border-collapse: collapse;}')
            with doc('body'):
                with doc('p'):
                    doc('a', 'Go to start page', href='/')
                with doc('table'):
                    doc('caption', 'Available commands')
                    for command, description in commands:
                        with doc('tr'):
                            doc('td', command)
                            doc('td', description)
        content = doc.content(with_html_stack.DEV_PARAMS)

        self.send_header('Content-Length', int(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def show_schema(self):
        svg = subprocess.check_output('./skeleton.sh _make_dot_file | dot -Tsvg', shell=True)

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'image/svg+xml; charset=us-ascii')
        self.send_header('Content-Length', int(len(svg)))
        self.end_headers()
        self.wfile.write(svg)

    def show_bad_path(self):
        self.send_response(HTTPStatus.NOT_FOUND)
        self.send_header('Content-Type', 'text/html')

        doc = with_html_stack.HTMLDocument()
        with doc('html', lang='en'):
            with doc('head'):
                doc('title', 'Error: path not found')
                doc('meta', _http_equiv='Content-type', content='text/html; charset=utf-8')
            with doc('body'):
                doc('h1', 'Error: path not found')
                doc('p', 'No path found on server: ' + escape(self.path))
                doc('a', 'Go to start page', href='/')
        content = doc.content(with_html_stack.DEV_PARAMS)

        self.send_header('Content-Length', int(len(content)))
        self.end_headers()
        self.wfile.write(content)


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass


def run(server_class=ThreadingHTTPServer, handler_class=SmallHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
