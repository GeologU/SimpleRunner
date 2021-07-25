import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from typing import Optional


class PreHandler(BaseHTTPRequestHandler):
    def return_content(
        self,
        status: HTTPStatus,
        content_type: str,
        content: bytes,
        headers: Optional[dict] = None,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))

        if headers is not None:
            for key, value in headers.items():
                self.send_header(key, value)
        self.end_headers()

        self.wfile.write(content)

    def read_data(self) -> Optional[bytes]:
        data_size = self.headers["Content-Length"]
        if data_size:
            return self.rfile.read(int(data_size))
        return None

    @property
    def host(self) -> str:
        host = self.headers["Host"]
        if "://" not in host:
            host = self.protocol_version.rsplit("/", 1)[0].lower() + "://" + host
        return host


class JSONHandler(PreHandler):
    def return_json(self, status: HTTPStatus, obj: dict) -> None:
        content = json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False).encode("UTF-8")
        self.return_content(status, "application/json", content)

    def read_json(self):
        data = self.read_data()
        if data is not None:
            return json.loads(data)
        return None
