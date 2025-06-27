from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_HOST: str = "mongodb:27017"
    MONGO_USER: str = "root"
    MONGO_PASSWORD: str = "abc123"
    MONGO_DB: str = "oj"
    REDIS_HOST: str = "redis-server"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
