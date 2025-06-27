from fastapi import FastAPI
from .routes import register_routes
from queue import Queue

def create_app() -> FastAPI:
    app = FastAPI()
    app.state.queue = Queue()
    register_routes(app)

    return app
