from http.server import BaseHTTPRequestHandler

from users import get_current_user, save_user, authenticate_user, logout
from utils import setup

log = setup()

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    # POST_REQUEST
    def do_POST(self):
        if self.path == "/sessions/register":
            save_user(self)
        elif self.path == "/sessions/login":
            authenticate_user(self)
        else:
            self.not_found()

        log.info(f'{self.client_address[0]} - - "POST {self.path}" 201')
    

    # GET_REQUEST
    def do_GET(self):
        if self.path == "/sessions/me":
            get_current_user(self);
        elif self.path == "/sessions/logout":
            logout(self);
        else:
            self.not_found()

        log.info(f'{self.client_address[0]} - - "GET {self.path}" 200')
    
    # BAD_REQUEST
    def not_found(self):
        self.send_response(404)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"error": "Resource Not Found"}')

        log.info(f'{self.client_address[0]} - - "GET {self.path}" 400S')