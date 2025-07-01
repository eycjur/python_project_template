"""
ホスト側でFlaskサーバーを起動し、Playwrightでテストを生成する

```shell
python -m app.presentation.flask.app &
playwright codegen
```
"""

import re
import subprocess
import sys
import time
from typing import Generator

import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session", autouse=True)
def flask_server() -> Generator[None, None, None]:
    """E2Eテスト用にFlaskサーバーをサブプロセスで起動する

    Yields:
        None
    """
    command = [
        sys.executable,  # 現在のPythonインタープリターを使用
        "-m",
        "app.presentation.flask.app",
    ]
    env = {
        "CONTAINER_PORT": "5000",
        "PYTEST_CURRENT_TEST": "1",  # テスト実行中のフラグを設定
    }

    with subprocess.Popen(command, env=env, text=True) as proc:  # noqa: S603
        time.sleep(2)  # サーバー起動待ち
        try:
            yield
        finally:
            proc.terminate()
            proc.wait()


def test_flask_index_page(page: Page) -> None:
    """Flaskトップページが正しく表示されることを検証する

    Args:
        page (Page): Playwrightのページオブジェクト
    """
    page.goto("http://localhost:5000/")
    expect(page).to_have_title(re.compile("履歴ページ"))


def test_flask_message_post(page: Page) -> None:
    """メッセージ投稿フォームのE2Eテスト

    Args:
        page (Page): Playwrightのページオブジェクト
    """
    # フォームのinput[name="user_input"]に値を入力し、送信
    page.goto("http://localhost:5000/register")
    page.fill('input[name="user_input"]', "test1")
    page.click('input[type="submit"]')

    # フォームのinput[name="user_input"]に値を入力し、送信
    page.goto("http://localhost:5000/register")
    page.fill('input[name="user_input"]', "test2")
    page.click('input[type="submit"]')

    # 投稿後、履歴ページに遷移
    page.goto("http://localhost:5000/home")

    # .message.card の要素をすべて取得
    messages = page.locator(".message-item")

    # 要素の数を検証
    expect(messages).to_have_count(2)

    expect(messages.nth(0)).to_have_text("test2")
    expect(messages.nth(1)).to_have_text("test1")
