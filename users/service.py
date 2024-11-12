import bcrypt
import secrets

from sqlalchemy.orm import Session
from .model import User

class UserService:
    def __init__(self, db: Session, data=None):
        self.data = db.query(User).filter(User.id == data["id"]).first() if data else db.query(User).all()
    
    @property
    def uuid(self):
        return self.data.uuid or ''
    
    @property
    def firstname(self):
        return self.data.firstname or ''

    @property
    def lastname(self):
        return self.data.lastname or ''

    @property
    def email(self):
        return self.data.email or ''

    def username(self):
        return f"{self.data.firstname} {self.data.lastname}" or ''

class UserController:
    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

    def handler_create_user(self, db: Session):
        existing_user = db.query(User).filter(User.email == self.email).first()
        if existing_user:
            raise ValueError("A user with this email address already exists.")

        hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = User(
            firstname=self.firstname,
            lastname=self.lastname,
            email=self.email,
            password=hashed_password
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def handler_authenticate_user(self, email, password):
        pass

    def generate_token():
        return secrets.token_hex(16)