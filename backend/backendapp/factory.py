from queue import Queue
import logging

import mongoengine as me
from fastapi import FastAPI

from app.services import UserService, ProblemService
from app.routes import register_routes, register_auth_routes, register_problem_routes
from config import Settings

def create_app() -> FastAPI:
    app = FastAPI()
    settings = Settings()
    
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    app.state.logger = logger

    app.state.queue = Queue()
    app.state.url = settings.BACKEND_URL

    mongo_connection = (
            "mongodb://"
            f"{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@"
            f"{settings.MONGO_HOST}"
    )
    me.connect(db=settings.MONGO_DB, host=mongo_connection)

    app.state.user_service = UserService(settings.JWT_SECRET)

    register_routes(app)
    register_auth_routes(app)

    problem_app = FastAPI()
    problem_app.state.problem_service = ProblemService
    register_problem_routes(problem_app)
    app.mount("/problems", problem_app)

    return app
