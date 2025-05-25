from typing import Generator

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from injector import Injector

from app.di import TestModule
from app.presentation.fastapi.app import app
from app.presentation.fastapi.controller.get_injector import get_injector


# セットアップとティアダウンを行うタイミングを指定できる
# scope:
#   session(1回だけ実行)
#   package(パッケージごとに1回)
#   module(モジュールごとに1回)
#   class(クラスごとに1回)
#   function(テスト関数ごとに1回)
@pytest.fixture
def injector() -> Injector:
    return Injector(TestModule())


@pytest.fixture
def client(injector: Injector) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_injector] = lambda: injector
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_register(client: TestClient) -> None:
    response = client.post("/messages", json={"content": "hello"})
    assert response.status_code == status.HTTP_200_OK


def test_history(client: TestClient) -> None:
    response = client.post("/messages", json={"content": "hello"})
    assert response.status_code == status.HTTP_200_OK
    response = client.get("/messages")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["messages"][0]["content"] == "hello"


def test_history2(client: TestClient) -> None:
    response = client.post("/messages", json={"content": "hello2"})
    assert response.status_code == status.HTTP_200_OK
    response = client.get("/messages")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["messages"][0]["content"] == "hello2"
