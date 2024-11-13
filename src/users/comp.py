import json
from .service import UserController
from utils import get_db_session, RequestHandler, logger


def save_user(handler):
    content_length = int(handler.headers["Content-Length"])
    formData = json.loads(handler.rfile.read(content_length).decode('utf-8'))
    # logger().info(f"POST request data: {formData}")

    # Get a database session and create an user instance
    with get_db_session() as session:
        user_controller = UserController(
            firstname=formData["firstname"],
            lastname=formData["lastname"],
            email=formData["email"],
            password=formData["password"]
        )

    # Call create_user method
    status, response = user_controller.handler_create_user(session)

    # Return response data and status
    RequestHandler._send_response(handler, status, response)       

def authenticate_user(handler):
    content_length = int(handler.headers["Content-Length"])
    formData = json.loads(handler.rfile.read(content_length).decode('utf-8'))
    # logger().info(f"POST request data: {formData}")

    email = formData["email"]
    password = formData["password"]

    # Get a database session
    db_session = next(get_db_session())

    # Call authenticate_user method
    status, response = UserController.handler_authenticate_user(email, password, db_session)

    # Return response data and status
    RequestHandler._send_response(handler, status, response)