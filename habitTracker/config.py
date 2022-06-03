from dotenv import dotenv_values

config = dotenv_values(".env")


class Config:
    """Base config for flask app."""

    SECRET_KEY = config.get("SECRET_KEY")
    DATABASE = config.get("DATABASE")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

class ProdConfig(Config):
    """App config for production"""

    ENV = 'production'
    TESTING = False
    DEBUG = False
    MONGO_URI = config.get("MONGO_URI")

class DevConfig(Config):
    """App config for development"""

    ENV = 'development'
    DEBUG = True
    TESTING = True
    MONGO_URI = config.get("DEV_MONGO_URI")

class TestConfig(DevConfig):
    """App config to test mongo connection
    """

    MONGO_URI = config.get("TEST_URI")