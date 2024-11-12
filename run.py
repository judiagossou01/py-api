from http.server import HTTPServer
from db import init_db

def run(server_class=HTTPServer, handler_class=''):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print("Starting server on port 8000...")
    httpd.serve_forever()


if __name__ == "__main__":
    init_db()
    run()