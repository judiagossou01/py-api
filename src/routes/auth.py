from http.server import BaseHTTPRequestHandler

from users import get_current_user, save_user, authenticate_user, logout
from utils import logger


class AuthRoutes(BaseHTTPRequestHandler):

    # POST_REQUEST
    def do_POST(self):
        logger().info(f"POST request for {self.path}")
        if self.path == "/sessions/register":
            save_user(self)
        elif self.path == "/sessions/login":
            authenticate_user(self)
        else:
            self.not_found()
    

    # GET_REQUEST
    def do_GET(self):
        logger().info(f"GET request for {self.path}")
        if self.path == "/sessions/me":
            get_current_user(self);
        elif self.path == "/sessions/logout":
            logout(self);
        else:
            self.not_found()
    
    # BAD_REQUEST
    def not_found(self):
        self.send_response(404)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"error": "Resource Not Found"}')
        
