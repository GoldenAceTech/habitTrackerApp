from typing import Generator
from flask import Flask, g
from flask.ctx import _AppCtxGlobals
from flask.testing import FlaskClient, FlaskCliRunner
from habitTracker import create_app
from habitTracker.config import ProdConfig
import pytest


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    """Get the flask app with test configurations

    Yields:
        Generator[Flask, None, None]: Flask app
    """
    app = create_app()
    yield app

@pytest.fixture
def prod_app() -> Generator[Flask, None, None]:
    """Get the flask app with test configurations

    Yields:
        Generator[Flask, None, None]: Flask app
    """
    app = create_app(ProdConfig)
    yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """creates a test client for the application

    Args:
        app (Flask): The app Flask object

    Returns:
        FlaskClient: A flask test client that works like the app but for testing
    """
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def global_var(client: FlaskClient, app: Flask) -> _AppCtxGlobals:
    """get the application global context var
    """

    client.get("/")
    g.habits = [habit for habit in app.db.habits.find()]
    return g



@pytest.fixture
def runner(app:Flask) -> FlaskCliRunner:
    """creates a runner that can call the Click commands registered with the application

    Args:
        app (Flask): The app Flask object

    Returns:
        FlaskCliRunner: an instance of test_cli_runner_class
    """
    return app.test_cli_runner()
