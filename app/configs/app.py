from pydantic_settings import SettingsConfigDict
from dotenv import load_dotenv
from . import mongodb
import os

load_dotenv()


class AppSettings():
    app_env: str
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    # secret_key: str
    # mq_url: str
    # queue_name: str
    # model_config = SettingsConfigDict()


settings = AppSettings()
