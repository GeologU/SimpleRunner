#!/usr/bin/env python3

from html import escape
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from http import HTTPStatus
import subprocess

import with_html


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

        page = with_html.HTMLNode()
        page.tagl('!DOCTYPE', xxhtml=None)
        page.rawl('')
        html = page.tagb('html')

        with html.tagb('head') as h:
            h.tagl('title', 'Select your task')
            h.tagl('meta', xxhttp_equiv='Content-type', content='text/html; charset=utf-8')

        html.rawl('')
        with html.tagb('body') as b:
            with b.tagl('p') as p:
                p.tagc('a', 'View commands', href='/command/')
            with b.tagl('p') as p:
                p.tagc('a', 'View dependencies of commands', href='/schema/')

        content = bytes(page.text(with_html.TextParams()), 'UTF-8')

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

        page = with_html.HTMLNode()
        page.tagl('!DOCTYPE', xxhtml=None)
        page.rawl('')
        html = page.tagb('html')

        with html.tagb('head') as h:
            h.tagl('title', 'Select your task')
            h.tagl('meta', xxhttp_equiv='Content-type', content='text/html; charset=utf-8')
            with h.tagb('style', xxtype='text/css') as s:
                s.rawl('table, td {border: 1px solid gray; border-collapse: collapse;}')

        html.rawl('')
        with html.tagb('body') as b:
            with b.tagl('p') as p:
                p.tagc('a', 'Go to start page', href='/')
            with b.tagb('table') as table:
                table.tagl('caption', 'Available commands')
                for command, description in commands:
                    with table.tagl('tr') as row:
                        row.tagc('td', command)
                        row.tagc('td', description)

        content = bytes(page.text(with_html.TextParams()), 'UTF-8')

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

        page = with_html.HTMLNode()
        page.tagl('!DOCTYPE', xxhtml=None)
        page.rawl('')
        html = page.tagb('html')

        with html.tagb('head') as h:
            h.tagl('title', 'Error: path not found')
            h.tagl('meta', xxhttp_equiv='Content-type', content='text/html; charset=utf-8')

        html.rawl('')
        with html.tagb('body') as b:
            b.tagl('h1', 'Error: path not found')
            b.tagl('p', 'No path found on server: ' + escape(self.path))
            b.tagl('a', 'Go to start page', href='/')

        content = bytes(page.text(with_html.TextParams()), 'UTF-8')

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
