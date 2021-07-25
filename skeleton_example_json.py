#!/usr/bin/env python3

import datetime
import random
import sys
import threading
import time
from http import HTTPStatus
from http.server import ThreadingHTTPServer

from skeleton import JSONHandler


class ExampleHanler(JSONHandler):
    def do_GET(self):
        self.do_POST()

    def do_POST(self):
        try:
            if self.path == "/":
                self.show_index()
            elif self.path == "/sleep":
                self.show_sleep()
            else:
                self.show_bad_path()
        except Exception as exc:
            self.show_exception(exc)

    def show_bad_path(self):
        return self.return_json(
            HTTPStatus.NOT_FOUND,
            {
                "error": {
                    "message": "No path found on server: " + self.path,
                },
                "nagivation": {
                    "index": self.host + "/",
                },
            },
        )

    def show_exception(self, exc):
        return self.return_json(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            {
                "error": {
                    "message": "Internal server error",
                    "details": str(exc),
                },
                "nagivation": {
                    "index": self.host + "/",
                },
            },
        )

    def show_index(self):
        # FYI: Firefox can conveniently display JSON.
        # In particular, you can click on the links as on a regular HTML page.
        return self.return_json(
            HTTPStatus.OK,
            {
                "nagivation": {
                    "sleeper": self.host + "/sleep",
                },
            },
        )

    def show_sleep(self):
        to_sleep = 0.5 + random.random()
        self.log_message("sleep: %.2f\tstarted at: %s", to_sleep, datetime.datetime.now())
        time.sleep(to_sleep)
        self.log_message("sleep: %.2f\tfinished at: %s", to_sleep, datetime.datetime.now())
        return self.return_json(
            HTTPStatus.OK,
            {
                "sleeper": {
                    "slept": to_sleep,
                    "units": "seconds",
                    "thread": threading.get_ident(),
                },
                "nagivation": {
                    "index": self.host + "/",
                },
            },
        )


def run():
    address = ("localhost", 8001)
    print(f"Running at {address}", file=sys.stderr)
    httpd = ThreadingHTTPServer(address, ExampleHanler)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
