from typing import Optional
from datetime import datetime, timedelta

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from passlib.hash import bcrypt

from mongoengine import DoesNotExist

from ..models import User

class UserService:

    def __init__(self, jwt_secret):
        self.jwt_secret = jwt_secret

    def register(self, name: str, email: str, password: str) -> User:
        hashed_pw = bcrypt.hash(password)
        user = User(name=name, email=email, hashed_password=hashed_pw, status=1).save()
        return user

    def login(self, login: str, password: str) -> Optional[str]:
        user = User.objects(email=login).first() or User.objects(name=login).first()
        if user is None:
            return None
        if bcrypt.verify(password, user.hashed_password):
            payload = {
                "sub": str(user.id),
                "username": user.name,
                "email": user.email,
                "status": user.status,
                "exp": datetime.utcnow() + timedelta(minutes=86400)
            }
            token = jwt.encode(payload, self.jwt_secret, algorithm="HS256")
            return token
        return None

    def verify_token(self, token: str) -> Optional[User]:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            user_id = payload.get("sub")
            return User.objects.get(id=int(user_id))
        except (ExpiredSignatureError, InvalidTokenError, DoesNotExist):
            return None
