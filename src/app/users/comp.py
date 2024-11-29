import json
from .service import UserController
from app.utils import get_db_session, RequestHandler

SESSIONS = {}

def get_current_user(handler):
    auth_header = handler.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        RequestHandler._send_response(handler, 401, {"error": "Token is missing or invalid"})
        return 401

    token = auth_header.split(" ")[1]

    # Check whether token is valid
    user = SESSIONS.get(token)
    if not user:
        RequestHandler._send_response(handler, 401, {"error": "Token is invalid or expired"})
        return 401

    # Return current user
    RequestHandler._send_response(handler, 200, {"user": user})

    return 200

def save_user(handler):
    content_length = int(handler.headers["Content-Length"])
    formData = json.loads(handler.rfile.read(content_length).decode('utf-8'))

    # Get a database session and create an user instance
    db_session = next(get_db_session())
    user_controller = UserController(
        firstname=formData["firstname"],
        lastname=formData["lastname"],
        email=formData["email"],
        password=formData["password"]
    )    

    # Call create_user method
    status, response = user_controller.handler_create_user(db_session)

    # Return response data and status
    RequestHandler._send_response(handler, status, response)  

    return status 

def authenticate_user(handler):
    content_length = int(handler.headers["Content-Length"])
    formData = json.loads(handler.rfile.read(content_length).decode('utf-8'))

    email = formData["email"]
    password = formData["password"]

    # Get a database session
    db_session = next(get_db_session())

    # Call authenticate_user method
    status, response = UserController.handler_authenticate_user(email, password, db_session)
    if status == 200:
        token = response["token"]
        user_data = response["user"]

        # Add user data and token in SESSIONS
        SESSIONS[token] = user_data

    # Return response data and status
    RequestHandler._send_response(handler, status, response)

    return status

def logout(handler):
    auth_header = handler.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        RequestHandler._send_response(handler, 401, {"error": "Token is missing or invalid"})
        return 401

    token = auth_header.split(" ")[1]

    # Remove token from SESSIONS
    if token in SESSIONS:
        del SESSIONS[token]
        RequestHandler._send_response(handler, 200, {"message": "User logged out successfully"})
        return 200

    RequestHandler._send_response(handler, 401, {"error": "Token is invalid or expired"})
    return 401