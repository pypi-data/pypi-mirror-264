import pytest
from flask import Flask


@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "1"
    yield app


@pytest.fixture
def client(app):
    return app.test_client()
