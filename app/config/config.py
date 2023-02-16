import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    MONGO_INITDB_DATABASE: str = os.getenv("MONGO_INITDB_DATABASE")
    API_KEY: str = os.getenv("API_KEY")
    SECRET: str = os.getenv("SECRET")
    ACCESS_TOKEN: str = os.getenv("ACCESS_TOKEN")

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '../../.env')
