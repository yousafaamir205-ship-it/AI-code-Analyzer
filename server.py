"""Local web front end for the code analyzer. No extra dependencies.

    python server.py            ->  http://127.0.0.1:8000
    python server.py 9000       ->  custom port
"""

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from analyzer.report import analyze_source

INDEX = Path(__file__).parent / "web" / "index.html"
MAX_BYTES = 500_000


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body, content_type):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status, payload):
        self._send(status, json.dumps(payload).encode(), "application/json")

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, INDEX.read_bytes(), "text/html; charset=utf-8")
        else:
            self._json(404, {"ok": False, "error": {"message": "Not found"}})

    def do_POST(self):
        if self.path != "/api/analyze":
            return self._json(404, {"ok": False, "error": {"message": "Not found"}})

        length = int(self.headers.get("Content-Length", 0))
        if length > MAX_BYTES:
            return self._json(413, {"ok": False, "error": {"message": "File is too large (500 KB max)."}})

        try:
            data = json.loads(self.rfile.read(length) or b"{}")
            code = data.get("code", "")
            if not isinstance(code, str) or not code.strip():
                raise ValueError
        except ValueError:
            return self._json(400, {"ok": False, "error": {"message": "Send Python code in the 'code' field."}})

        self._json(200, analyze_source(code))

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"Code Analyzer running at http://127.0.0.1:{port}  (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
