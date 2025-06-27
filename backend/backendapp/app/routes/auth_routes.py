from fastapi import FastAPI, Request, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterForm(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginForm(BaseModel):
    login: str
    password: str

def register_auth_routes(app: FastAPI):

    @app.post("/register")
    def register(form: RegisterForm):
        try:
            user = app.state.user_service.register(form.name, form.email, form.password)
            return {"message": "User registered successfully", "user_id": user.id}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.post("/login")
    def login(form: LoginForm):
        token = app.user_service.login(form.login, form.password)
        if token:
            return {"access_token": token, "token_type": "bearer"}
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
