from typing import Optional
from datetime import datetime, timedelta

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from passlib.hash import bcrypt

from mongoengine import DoesNotExist

from ..models import User

class UserService:
    @staticmethod
    def register(name: str, email: str, password: str) -> User:
        hashed_pw = bcrypt.hash(password)
        user = User(name=name, email=email, hashed_password=hashed_pw, status=1).save()
        return user

    @staticmethod
    def login_by_email(login: str, password: str) -> Optional[str]:
        try:
            user = User.objects.get(email=login)
            if user is None:
                user = User.object.get(name=login)
            if user is None:
                return None
            if bcrypt.verify(password, user.hashed_password):
                payload = {
                    "sub": str(user.id),
                    "username": user.name,
                    "email": user.email,
                    "status": user.status,
                    "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
                }
                token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
                return token
            return None
        except DoesNotExist:
            return None

    @staticmethod
    def verify_token(token: str) -> Optional[User]:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            user_id = payload.get("sub")
            return User.objects.get(id=int(user_id))
        except (ExpiredSignatureError, InvalidTokenError, DoesNotExist):
            return None

