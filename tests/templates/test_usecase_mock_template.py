"""ユースケースクラスのモックテストテンプレート

このファイルは、ユースケースクラスの依存関係をモックしてテストを行う際のテンプレートです。
実際のテストでは、このファイルをコピーして必要に応じて修正してください。
"""

from unittest.mock import Mock

import pytest

from app.domain.message.message import Message
from app.domain.message.message_repository import IMessageRepository
from app.usecase.register import RegisterUsecase
from app.usecase.history import HistoryUsecase


class TestUsecaseMockTemplate:
    """ユースケースのモックテストのテンプレートクラス"""

    @pytest.fixture
    def mock_message_repository(self) -> Mock:
        """モックメッセージリポジトリのフィクスチャ
        
        Returns:
            Mock: IMessageRepositoryのモック
        """
        mock = Mock(spec=IMessageRepository)
        return mock

    @pytest.fixture
    def register_usecase(self, mock_message_repository: Mock) -> RegisterUsecase:
        """RegisterUsecaseのフィクスチャ（モックリポジトリを注入）
        
        Args:
            mock_message_repository: モックリポジトリ
            
        Returns:
            RegisterUsecase: テスト対象のユースケース
        """
        return RegisterUsecase(mock_message_repository)

    @pytest.fixture
    def history_usecase(self, mock_message_repository: Mock) -> HistoryUsecase:
        """HistoryUsecaseのフィクスチャ（モックリポジトリを注入）
        
        Args:
            mock_message_repository: モックリポジトリ
            
        Returns:
            HistoryUsecase: テスト対象のユースケース
        """
        return HistoryUsecase(mock_message_repository)

    def test_register_calls_repository_upsert(
        self, 
        register_usecase: RegisterUsecase, 
        mock_message_repository: Mock
    ) -> None:
        """メッセージ登録時にリポジトリのupsertが呼ばれることを確認"""
        # Arrange
        content = "テストメッセージ"
        
        # Act
        register_usecase.handle(content)
        
        # Assert
        mock_message_repository.upsert.assert_called_once()
        # 引数として渡されたMessageオブジェクトの内容を確認
        called_message = mock_message_repository.upsert.call_args[0][0]
        assert isinstance(called_message, Message)
        assert called_message.content == content

    def test_history_calls_repository_find_all(
        self, 
        history_usecase: HistoryUsecase, 
        mock_message_repository: Mock
    ) -> None:
        """履歴取得時にリポジトリのfind_allが呼ばれることを確認"""
        # Arrange
        expected_messages = [
            Message("メッセージ1"),
            Message("メッセージ2"),
        ]
        mock_message_repository.find_all.return_value = expected_messages
        
        # Act
        result = history_usecase.handle()
        
        # Assert
        mock_message_repository.find_all.assert_called_once()
        assert result == expected_messages

    def test_history_with_limit(
        self, 
        history_usecase: HistoryUsecase, 
        mock_message_repository: Mock
    ) -> None:
        """履歴取得時にlimitパラメータが正しく渡されることを確認"""
        # Arrange
        limit = 5
        expected_messages = [Message(f"メッセージ{i}") for i in range(limit)]
        mock_message_repository.find_all.return_value = expected_messages
        
        # Act
        result = history_usecase.handle(limit)
        
        # Assert
        mock_message_repository.find_all.assert_called_once_with(limit)
        assert len(result) == limit

    def test_register_with_empty_content(
        self, 
        register_usecase: RegisterUsecase, 
        mock_message_repository: Mock
    ) -> None:
        """空文字でのメッセージ登録テスト"""
        # Arrange
        content = ""
        
        # Act
        register_usecase.handle(content)
        
        # Assert
        mock_message_repository.upsert.assert_called_once()
        called_message = mock_message_repository.upsert.call_args[0][0]
        assert called_message.content == ""

    def test_repository_exception_propagation(
        self, 
        register_usecase: RegisterUsecase, 
        mock_message_repository: Mock
    ) -> None:
        """リポジトリで発生した例外がユースケースから伝播することを確認"""
        # Arrange
        mock_message_repository.upsert.side_effect = Exception("データベース接続エラー")
        
        # Act & Assert
        with pytest.raises(Exception, match="データベース接続エラー"):
            register_usecase.handle("テストメッセージ")

    @pytest.mark.parametrize("content,expected", [
        ("通常のメッセージ", "通常のメッセージ"),
        ("", ""),
        ("特殊文字!@#$%^&*()", "特殊文字!@#$%^&*()"),
        ("改行\nありメッセージ", "改行\nありメッセージ"),
    ])
    def test_register_various_content(
        self, 
        register_usecase: RegisterUsecase, 
        mock_message_repository: Mock,
        content: str,
        expected: str
    ) -> None:
        """様々な内容のメッセージ登録テスト（パラメータ化テスト例）"""
        # Act
        register_usecase.handle(content)
        
        # Assert
        mock_message_repository.upsert.assert_called_once()
        called_message = mock_message_repository.upsert.call_args[0][0]
        assert called_message.content == expected