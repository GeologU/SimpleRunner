#!/usr/bin/env python3

import subprocess
import sys
from html import escape
from http import HTTPStatus
from http.server import ThreadingHTTPServer

import with_html_stack
from skeleton import PreHandler


class HTMLHandlerExample(PreHandler):
    def do_GET(self):
        self.do_POST()

    def do_POST(self):
        if self.path == "/":
            self.show_index()
        elif self.path == "/command/":
            self.show_commands()
        elif self.path == "/schema/":
            self.show_schema()
        elif self.path == "/favicon.ico":
            self.return_content(HTTPStatus.NOT_FOUND, "text/plain", b"")
        else:
            self.show_bad_path()

    def show_index(self):
        doc = with_html_stack.HTMLDocument()
        with doc("html", lang="en"):
            with doc("head"):
                doc("title", "Select your task")
                doc("meta", _http_equiv="Content-type", content="text/html; charset=utf-8")
            with doc("body"):
                with doc("p"):
                    doc("a", "View commands", href="/command/")
                with doc("p"):
                    doc("a", "View dependencies of commands", href="/schema/")

        content = doc.content(with_html_stack.DEV_PARAMS)
        self.return_content(HTTPStatus.OK, "text/html", content)

    def show_commands(self):
        commands = []
        output = subprocess.check_output(["./skeleton.sh", "usage"]).decode()
        for item in output.splitlines():
            cols = item.split(maxsplit=1)
            if len(cols) == 2:
                commands.append(cols)

        doc = with_html_stack.HTMLDocument()
        with doc("html", lang="en"):
            with doc("head"):
                doc("title", "Select your task")
                doc("meta", _http_equiv="Content-type", content="text/html; charset=utf-8")
                with doc("style"):
                    doc.raw("table, td {border: 1px solid gray; border-collapse: collapse;}")
            with doc("body"):
                with doc("p"):
                    doc("a", "Go to start page", href="/")
                with doc("table"):
                    doc("caption", "Available commands")
                    for command, description in commands:
                        with doc("tr"):
                            doc("td", command)
                            doc("td", description)

        content = doc.content(with_html_stack.DEV_PARAMS)
        self.return_content(HTTPStatus.OK, "text/html", content)

    def show_schema(self):
        svg = subprocess.check_output("./skeleton.sh _make_dot_file | dot -Tsvg", shell=True)
        self.return_content(HTTPStatus.OK, "image/svg+xml; charset=us-ascii", svg)

    def show_bad_path(self):
        doc = with_html_stack.HTMLDocument()
        with doc("html", lang="en"):
            with doc("head"):
                doc("title", "Error: path not found")
                doc("meta", _http_equiv="Content-type", content="text/html; charset=utf-8")
            with doc("body"):
                doc("h1", "Error: path not found")
                doc("p", "No path found on server: " + escape(self.path))
                doc("a", "Go to start page", href="/")

        content = doc.content(with_html_stack.DEV_PARAMS)
        self.return_content(HTTPStatus.NOT_FOUND, "text/html", content)


def run():
    address = ("localhost", 8000)
    print(f"Running on {address}", file=sys.stderr)
    httpd = ThreadingHTTPServer(address, HTMLHandlerExample)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
