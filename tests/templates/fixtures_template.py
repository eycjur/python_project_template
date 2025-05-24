"""pytestフィクスチャのテンプレート

このファイルは、よく使用されるpytestフィクスチャのテンプレートです。
実際のテストでは、このファイルから必要なフィクスチャをコピーして使用してください。
"""

from typing import Any, Generator
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from injector import Injector

from app.di import TestModule
from app.domain.message.message import Message
from app.domain.message.message_repository import IMessageRepository
from app.presentation.fastapi.app import app
from app.presentation.fastapi.controller.get_injector import get_injector


# ========================================
# 基本的なフィクスチャ
# ========================================

@pytest.fixture
def sample_message() -> Message:
    """テスト用のサンプルメッセージ
    
    Returns:
        Message: テスト用メッセージ
    """
    return Message("テストメッセージ")


@pytest.fixture
def sample_messages() -> list[Message]:
    """テスト用の複数メッセージ
    
    Returns:
        list[Message]: テスト用メッセージリスト
    """
    return [
        Message("メッセージ1"),
        Message("メッセージ2"),
        Message("メッセージ3"),
    ]


# ========================================
# モック関連のフィクスチャ
# ========================================

@pytest.fixture
def mock_message_repository() -> Mock:
    """モックメッセージリポジトリ
    
    Returns:
        Mock: IMessageRepositoryのモック
    """
    mock = Mock(spec=IMessageRepository)
    return mock


@pytest.fixture
def mock_message_repository_with_data(sample_messages: list[Message]) -> Mock:
    """データを持つモックメッセージリポジトリ
    
    Args:
        sample_messages: テスト用メッセージリスト
        
    Returns:
        Mock: データを設定済みのIMessageRepositoryのモック
    """
    mock = Mock(spec=IMessageRepository)
    mock.find_all.return_value = sample_messages
    return mock


# ========================================
# 依存性注入関連のフィクスチャ
# ========================================

@pytest.fixture
def test_injector() -> Injector:
    """テスト用のDIコンテナ
    
    Returns:
        Injector: テスト用のInjector
    """
    return Injector(TestModule())


@pytest.fixture
def injector_with_mock_repository(mock_message_repository: Mock) -> Injector:
    """モックリポジトリを使用するDIコンテナ
    
    Args:
        mock_message_repository: モックリポジトリ
        
    Returns:
        Injector: モックリポジトリを設定したInjector
    """
    from injector import Module, Binder
    
    class MockModule(Module):
        def configure(self, binder: Binder) -> None:
            binder.bind(IMessageRepository, to=mock_message_repository)
    
    return Injector([MockModule()])


# ========================================
# FastAPI関連のフィクスチャ
# ========================================

@pytest.fixture
def test_client(test_injector: Injector) -> Generator[TestClient, None, None]:
    """FastAPIのテストクライアント
    
    Args:
        test_injector: テスト用のInjector
        
    Yields:
        TestClient: FastAPIのテストクライアント
    """
    app.dependency_overrides[get_injector] = lambda: test_injector
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def test_client_with_mock(
    injector_with_mock_repository: Injector
) -> Generator[TestClient, None, None]:
    """モックリポジトリを使用するFastAPIテストクライアント
    
    Args:
        injector_with_mock_repository: モックリポジトリを使用するInjector
        
    Yields:
        TestClient: FastAPIのテストクライアント
    """
    app.dependency_overrides[get_injector] = lambda: injector_with_mock_repository
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


# ========================================
# パラメータ化テスト用のフィクスチャ
# ========================================

@pytest.fixture(params=[
    "通常のメッセージ",
    "",
    "特殊文字!@#$%^&*()",
    "改行\nありメッセージ",
    "長いメッセージ" + "あ" * 1000,
])
def various_message_contents(request: Any) -> str:
    """様々な内容のメッセージ（パラメータ化テスト用）
    
    Args:
        request: pytestのrequestオブジェクト
        
    Returns:
        str: テスト用メッセージ内容
    """
    return request.param


@pytest.fixture(params=[1, 5, 10, 100])
def various_limits(request: Any) -> int:
    """様々なlimit値（パラメータ化テスト用）
    
    Args:
        request: pytestのrequestオブジェクト
        
    Returns:
        int: テスト用limit値
    """
    return request.param


# ========================================
# セットアップ・ティアダウン関連のフィクスチャ
# ========================================

@pytest.fixture
def setup_test_data() -> Generator[dict[str, Any], None, None]:
    """テストデータのセットアップとクリーンアップ
    
    テスト前にデータを準備し、テスト後にクリーンアップを行う例
    
    Yields:
        dict[str, Any]: テストデータ
    """
    # セットアップ
    test_data = {
        "messages": [
            Message("セットアップメッセージ1"),
            Message("セットアップメッセージ2"),
        ],
        "config": {"limit": 10}
    }
    
    try:
        yield test_data
    finally:
        # ティアダウン（クリーンアップ）
        # 必要に応じてデータベースのクリーンアップなどを行う
        pass


@pytest.fixture(scope="session")
def session_setup() -> Generator[None, None, None]:
    """セッション全体でのセットアップとティアダウン
    
    テストセッション開始時に一度だけ実行される
    
    Yields:
        None
    """
    # セッション開始時のセットアップ
    print("テストセッション開始")
    
    try:
        yield
    finally:
        # セッション終了時のティアダウン
        print("テストセッション終了")


@pytest.fixture(scope="module")
def module_setup() -> Generator[None, None, None]:
    """モジュール単位でのセットアップとティアダウン
    
    テストモジュール開始時に一度だけ実行される
    
    Yields:
        None
    """
    # モジュール開始時のセットアップ
    print("テストモジュール開始")
    
    try:
        yield
    finally:
        # モジュール終了時のティアダウン
        print("テストモジュール終了")