"""統合テスト（依存性注入使用）のテンプレート

このファイルは、依存性注入を使用した統合テストのテンプレートです。
実際のテストでは、このファイルから必要なパターンをコピーして使用してください。
"""

from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from injector import Injector, Module, Binder

from app.di import TestModule
from app.domain.message.message import Message
from app.domain.message.message_repository import IMessageRepository
from app.presentation.fastapi.app import app
from app.presentation.fastapi.controller.get_injector import get_injector
from app.usecase.register import RegisterUsecase
from app.usecase.history import HistoryUsecase


class TestIntegrationTemplate:
    """統合テストのテンプレートクラス"""

    # ========================================
    # 実際のTestModuleを使用した統合テスト
    # ========================================

    @pytest.fixture
    def real_injector(self) -> Injector:
        """実際のTestModuleを使用するInjector
        
        Returns:
            Injector: TestModuleを使用したInjector
        """
        return Injector(TestModule())

    @pytest.fixture
    def real_test_client(self, real_injector: Injector) -> TestClient:
        """実際のTestModuleを使用するFastAPIテストクライアント
        
        Args:
            real_injector: 実際のTestModuleを使用するInjector
            
        Returns:
            TestClient: FastAPIのテストクライアント
        """
        app.dependency_overrides[get_injector] = lambda: real_injector
        return TestClient(app)

    def test_real_integration_post_and_get_messages(
        self, 
        real_test_client: TestClient
    ) -> None:
        """実際のTestModuleを使用した統合テスト（POST→GET）"""
        # Arrange
        test_content = "統合テストメッセージ"
        
        # Act: メッセージを投稿
        post_response = real_test_client.post("/messages", json={"content": test_content})
        
        # Assert: 投稿が成功
        assert post_response.status_code == 200
        
        # Act: メッセージリストを取得
        get_response = real_test_client.get("/messages")
        
        # Assert: 取得が成功し、投稿したメッセージが含まれている
        assert get_response.status_code == 200
        messages = get_response.json()["messages"]
        assert len(messages) > 0
        assert any(msg["content"] == test_content for msg in messages)

    def test_real_integration_multiple_messages(
        self, 
        real_test_client: TestClient
    ) -> None:
        """複数メッセージの投稿と取得テスト"""
        # Arrange
        test_contents = ["メッセージ1", "メッセージ2", "メッセージ3"]
        
        # Act: 複数メッセージを投稿
        for content in test_contents:
            response = real_test_client.post("/messages", json={"content": content})
            assert response.status_code == 200
        
        # Act: メッセージリストを取得
        get_response = real_test_client.get("/messages")
        
        # Assert: すべてのメッセージが取得できる
        assert get_response.status_code == 200
        messages = get_response.json()["messages"]
        retrieved_contents = [msg["content"] for msg in messages]
        
        for content in test_contents:
            assert content in retrieved_contents

    # ========================================
    # モックを部分的に使用した統合テスト
    # ========================================

    @pytest.fixture
    def mock_repository(self) -> Mock:
        """モックリポジトリ
        
        Returns:
            Mock: IMessageRepositoryのモック
        """
        mock = Mock(spec=IMessageRepository)
        return mock

    @pytest.fixture
    def partial_mock_injector(self, mock_repository: Mock) -> Injector:
        """一部をモックに置き換えたInjector
        
        Args:
            mock_repository: モックリポジトリ
            
        Returns:
            Injector: 一部モック使用のInjector
        """
        class PartialMockModule(Module):
            def configure(self, binder: Binder) -> None:
                # ユースケースは実際のものを使用
                binder.bind(RegisterUsecase, to=RegisterUsecase)
                binder.bind(HistoryUsecase, to=HistoryUsecase)
                # リポジトリのみモックを使用
                binder.bind(IMessageRepository, to=mock_repository)
        
        return Injector([PartialMockModule()])

    @pytest.fixture
    def partial_mock_client(self, partial_mock_injector: Injector) -> TestClient:
        """一部モックを使用するFastAPIテストクライアント
        
        Args:
            partial_mock_injector: 一部モック使用のInjector
            
        Returns:
            TestClient: FastAPIのテストクライアント
        """
        app.dependency_overrides[get_injector] = lambda: partial_mock_injector
        return TestClient(app)

    def test_partial_mock_integration_post_message(
        self, 
        partial_mock_client: TestClient, 
        mock_repository: Mock
    ) -> None:
        """一部モックを使用した統合テスト（POST）"""
        # Arrange
        test_content = "モック統合テストメッセージ"
        
        # Act
        response = partial_mock_client.post("/messages", json={"content": test_content})
        
        # Assert
        assert response.status_code == 200
        # モックリポジトリのupsertが呼ばれることを確認
        mock_repository.upsert.assert_called_once()
        called_message = mock_repository.upsert.call_args[0][0]
        assert isinstance(called_message, Message)
        assert called_message.content == test_content

    def test_partial_mock_integration_get_messages(
        self, 
        partial_mock_client: TestClient, 
        mock_repository: Mock
    ) -> None:
        """一部モックを使用した統合テスト（GET）"""
        # Arrange
        expected_messages = [
            Message("モックメッセージ1"),
            Message("モックメッセージ2"),
        ]
        mock_repository.find_all.return_value = expected_messages
        
        # Act
        response = partial_mock_client.get("/messages")
        
        # Assert
        assert response.status_code == 200
        mock_repository.find_all.assert_called_once()
        
        messages = response.json()["messages"]
        assert len(messages) == 2
        assert messages[0]["content"] == "モックメッセージ1"
        assert messages[1]["content"] == "モックメッセージ2"

    # ========================================
    # エラーケースの統合テスト
    # ========================================

    def test_integration_repository_error_handling(
        self, 
        partial_mock_client: TestClient, 
        mock_repository: Mock
    ) -> None:
        """リポジトリエラーが適切に処理されることを確認"""
        # Arrange
        mock_repository.upsert.side_effect = Exception("データベース接続エラー")
        
        # Act
        response = partial_mock_client.post("/messages", json={"content": "テスト"})
        
        # Assert
        # エラーハンドリングの実装に応じて調整
        assert response.status_code == 500

    def test_integration_invalid_request_data(
        self, 
        real_test_client: TestClient
    ) -> None:
        """無効なリクエストデータの処理テスト"""
        # Act & Assert
        # 必須フィールドが欠けている場合
        response = real_test_client.post("/messages", json={})
        assert response.status_code == 422  # Validation Error
        
        # 無効なデータ型の場合
        response = real_test_client.post("/messages", json={"content": 123})
        assert response.status_code == 422  # Validation Error

    # ========================================
    # パフォーマンステスト
    # ========================================

    def test_integration_performance_multiple_requests(
        self, 
        real_test_client: TestClient
    ) -> None:
        """複数リクエストのパフォーマンステスト"""
        import time
        
        # Arrange
        request_count = 10
        max_total_time = 5.0  # 5秒以内
        
        # Act
        start_time = time.time()
        for i in range(request_count):
            response = real_test_client.post("/messages", json={"content": f"メッセージ{i}"})
            assert response.status_code == 200
        end_time = time.time()
        
        # Assert
        total_time = end_time - start_time
        assert total_time < max_total_time, f"パフォーマンステスト失敗: {total_time}秒 > {max_total_time}秒"

    # ========================================
    # セットアップ・ティアダウンを含む統合テスト
    # ========================================

    @pytest.fixture
    def isolated_test_environment(self) -> Injector:
        """分離されたテスト環境のセットアップ
        
        Returns:
            Injector: 分離されたテスト環境のInjector
        """
        # テスト専用の設定でInjectorを作成
        injector = Injector(TestModule())
        
        # 必要に応じて初期データのセットアップなどを行う
        # repository = injector.get(IMessageRepository)
        # repository.upsert(Message("初期データ"))
        
        return injector

    def test_integration_with_isolated_environment(
        self, 
        isolated_test_environment: Injector
    ) -> None:
        """分離された環境での統合テスト"""
        # Arrange
        app.dependency_overrides[get_injector] = lambda: isolated_test_environment
        client = TestClient(app)
        
        try:
            # Act & Assert
            response = client.post("/messages", json={"content": "分離環境テスト"})
            assert response.status_code == 200
            
            response = client.get("/messages")
            assert response.status_code == 200
            
        finally:
            # ティアダウン
            app.dependency_overrides.clear()