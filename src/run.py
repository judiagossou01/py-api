import sys
import os

from http.server import HTTPServer
from art import text2art

from app.utils import init_db
from app import MyHTTPRequestHandler

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

def run(server_class=HTTPServer, handler_class=MyHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print("Starting server on port 8000...")
    httpd.serve_forever()

def api_name():
    ascii_art = text2art("PY-API")
    print(ascii_art)


if __name__ == "__main__":
    print("Starting application...")
    
    # Database initialization
    init_db()
    print("Database initialized.")
    
    api_name()
    
    # Run server
    run()
    print("Application is now running!")