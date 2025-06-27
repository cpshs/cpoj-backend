from fastapi import FastAPI, Request

def register_routes(app: FastAPI):

    @app.get("/")
    def hello():
        return {"message": "Greeting From CPOJ Backend."}

