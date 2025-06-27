from fastapi import FastAPI, Request
from ..services import UserService

def register_routes(app: FastAPI):

    @app.get("/login")
    def hello():
        return {"message": "Greeting From CPOJ Backend."}

