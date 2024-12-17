from http.server import BaseHTTPRequestHandler
import json

class RequestHandler(BaseHTTPRequestHandler):

    def _send_response(self, status, content):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(content).encode("utf-8"))