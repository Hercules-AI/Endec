from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGODB_USERNAME: str
    MONGODB_PASSWORD: str
    MONGODB_HOST: str
    MONGODB_DATABASE: str
