from flask import Flask
from pymongo.database import Database
from habitTracker import config, create_app


def test_config(app: Flask, prod_app: Flask) -> None:
    """Test for the configuration, to ensure database connection establish correctly and the flask app runs with the right configurations

    Args:
        app (Flask): The flask application
    """
    # test the development config
    assert app.config["ENV"] == "development"
    assert isinstance(app.db, Database)
    # test the production config
    assert prod_app.config["ENV"] == "production"
    assert isinstance(prod_app.db, Database)
    #test for a wrong db_uri
    error_message = create_app(config.TestConfig).db
    assert isinstance(error_message, str)