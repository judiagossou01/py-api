import traceback
from http.server import BaseHTTPRequestHandler

from .users import get_current_user, save_user, authenticate_user, logout
from .utils import initialize_logger, log_message

# Initialize logs configuration
log = initialize_logger()

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    
    # Set CORS headers
    def add_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS") 
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    # Set OPTIONS request
    def do_OPTIONS(self):
        self.send_response(200)
        self.add_cors_headers()
        self.end_headers()


    
    # Set POST request
    def do_POST(self):
        try:
            if self.path == "/sessions/register":
                req = save_user(self)
            elif self.path == "/sessions/login":
                req = authenticate_user(self)
            else:
                req = self.not_found()
        except Exception as e:
            error_details = traceback.format_exc()
            log.error(f"Server Error: {e}, Path: {self.path}\nDetails:\n{error_details}")

        self.add_cors_headers()
        log_message(
            log,
            "PY-API",
            extra={
                "client_ip": self.client_address[0],
                "method": self.command,
                "path": self.path,
                "protocol": self.request_version,
                "status": req,
            }
        )
    

    # Set GET request
    def do_GET(self):
        try:
            if self.path == "/sessions/me":
                req = get_current_user(self);
            elif self.path == "/sessions/logout":
                req = logout(self);
            else:
                req = self.not_found()
        except Exception as e:
            error_details = traceback.format_exc()
            log.error(f"Server Error: {e}, Path: {self.path}\nDetails:\n{error_details}")

        self.add_cors_headers()
        log_message(
            log,
            "PY-API",
            extra={
                "client_ip": self.client_address[0],
                "method": self.command,
                "path": self.path,
                "protocol": self.request_version,
                "status": req,
            }
        )

    
    # Set BAD request
    def not_found(self):
        self.send_response(404)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"error": "Resource Not Found"}')

        return 404