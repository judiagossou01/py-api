from http.server import BaseHTTPRequestHandler

from users import save_user, authenticate_user
from utils import logger


class AuthRoutes(BaseHTTPRequestHandler):
    # POST REQUEST
    def do_POST(self):
        logger().info(f"POST request for {self.path}")
        if self.path == "/sessions/register":
            save_user(self)
        elif self.path == "/sessions/login":
            authenticate_user(self)
    


        
