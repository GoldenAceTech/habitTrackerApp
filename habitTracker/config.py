from dotenv import load_dotenv
from os import environ

load_dotenv()


class Config:
    """Base config for flask app."""

    SECRET_KEY = environ.get("SECRET_KEY")
    DATABASE = environ.get("DATABASE")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

class ProdConfig(Config):
    """App config for production"""

    ENV = 'production'
    TESTING = False
    DEBUG = False
    MONGO_URI = environ.get("MONGO_URI")

class DevConfig(Config):
    """App config for development"""

    ENV = 'development'
    DEBUG = True
    TESTING = True
    MONGO_URI = environ.get("DEV_MONGO_URI")

class TestConfig(DevConfig):
    """App config to test mongo connection
    """

    MONGO_URI = environ.get("TEST_URI")

app_config = DevConfig
if environ.get("FLASK_ENV") == "production":
    app_config = ProdConfig