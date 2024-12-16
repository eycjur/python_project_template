import pytest
from fastapi.testclient import TestClient
from injector import Injector

from src.di import TestModule
from src.presentation.fastapi.app import app
from src.presentation.fastapi.controller.get_injector import get_injector


@pytest.fixture()
def injector() -> Injector:
    return Injector(TestModule())


@pytest.fixture()
def client(injector: Injector) -> TestClient:
    app.dependency_overrides[get_injector] = lambda: injector
    return TestClient(app)


def test_register(client: TestClient) -> None:
    response = client.post("/messages", json={"content": "hello"})
    assert response.status_code == 200


def test_history(client: TestClient) -> None:
    response = client.get("/messages")
    assert response.status_code == 200
    assert response.json() == {"messages": []}
    response = client.post("/messages", json={"content": "hello"})
    assert response.status_code == 200
    response = client.get("/messages")
    assert response.status_code == 200
    assert response.json() == {"messages": [{"content": "hello"}]}


def test_history2(client: TestClient) -> None:
    response = client.get("/messages")
    assert response.status_code == 200
    assert response.json() == {"messages": []}
    response = client.post("/messages", json={"content": "hello2"})
    assert response.status_code == 200
    response = client.get("/messages")
    assert response.status_code == 200
    assert response.json() == {"messages": [{"content": "hello2"}]}
