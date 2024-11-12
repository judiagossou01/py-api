import json
from http.server import BaseHTTPRequestHandler

from db import get_db_session
from users.service import UserController


class AuthRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == "/sessions/register":
            self.save_user(self)
        elif self.path == "/sessions/login":
            self.authenticate_user(self)

    def save_user(self):
        content_length = int(self.headers["Content-Length"])
        formData = json.loads(self.rfile.read(content_length))

        with get_db_session() as session:
            user_controller = UserController(
                firstname=formData["firstname"],
                lastname=formData["lastname"],
                email=formData["email"],
                password=formData["password"]
            )

        try:
            new_user = user_controller.handler_create_user(session)
            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(
                json.dumps(
                    {
                        "id": new_user.uuid,
                        "message": "User registered successfully"
                    }
                ).encode('utf-8')
            )
        except ValueError as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def authenticate_user(self):
        content_length = int(self.headers['Content-Length'])
        formData = json.loads(self.rfile.read(content_length))

        email = formData.get("email")
        password = formData.get("password")

        if UserController.handler_authenticate_user(email, password):
            token = UserController.generate_token()
            self._send_response(200, {"token": token})
        else:
            self._send_response(401, {"error": "Unauthorized"})


        
