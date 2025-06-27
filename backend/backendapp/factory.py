from queue import Queue

import mongoengine as me
from fastapi import FastAPI

from routes import register_routes
from config import Settings

def create_app() -> FastAPI:
    app = FastAPI()
    settings = Settings()

    app.state.queue = Queue()

    mongo_connection = (
            "mongodb://"
            f"{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@"
            f"{settings.MONGO_HOST}"
    )
    me.connect(db=settings.MONGO_DB, host=mongo_connection)

    register_routes(app)
    
    return app
