"""リポジトリクラスのモックテストテンプレート

このファイルは、リポジトリクラスをモックしてテストを行う際のテンプレートです。
実際のテストでは、このファイルをコピーして必要に応じて修正してください。
"""

from unittest.mock import Mock, patch

import pytest

from app.domain.message.message import Message
from app.domain.message.message_repository import IMessageRepository


class TestRepositoryMockTemplate:
    """リポジトリのモックテストのテンプレートクラス"""

    @pytest.fixture
    def mock_repository(self) -> Mock:
        """モックリポジトリのフィクスチャ
        
        Returns:
            Mock: IMessageRepositoryのモック
        """
        mock = Mock(spec=IMessageRepository)
        return mock

    @pytest.fixture
    def sample_message(self) -> Message:
        """テスト用のサンプルメッセージ
        
        Returns:
            Message: テスト用メッセージ
        """
        return Message("テストメッセージ")

    def test_upsert_success(self, mock_repository: Mock, sample_message: Message) -> None:
        """upsertメソッドが正常に呼び出されることを確認するテスト"""
        # Act
        mock_repository.upsert(sample_message)
        
        # Assert
        mock_repository.upsert.assert_called_once_with(sample_message)

    def test_find_all_returns_messages(self, mock_repository: Mock) -> None:
        """find_allメソッドがメッセージリストを返すことを確認するテスト"""
        # Arrange
        expected_messages = [
            Message("メッセージ1"),
            Message("メッセージ2"),
        ]
        mock_repository.find_all.return_value = expected_messages
        
        # Act
        result = mock_repository.find_all()
        
        # Assert
        assert result == expected_messages
        mock_repository.find_all.assert_called_once()

    def test_find_all_with_limit(self, mock_repository: Mock) -> None:
        """find_allメソッドにlimitパラメータを渡すテスト"""
        # Arrange
        limit = 5
        expected_messages = [Message(f"メッセージ{i}") for i in range(limit)]
        mock_repository.find_all.return_value = expected_messages
        
        # Act
        result = mock_repository.find_all(limit=limit)
        
        # Assert
        assert len(result) == limit
        mock_repository.find_all.assert_called_once_with(limit=limit)

    @patch('app.infrastructure.repository.message.sqlite_message_repository.SQLiteMessageRepository')
    def test_repository_instantiation_mock(self, mock_sqlite_repo_class: Mock) -> None:
        """リポジトリクラスのインスタンス化をモックするテスト例"""
        # Arrange
        mock_instance = Mock(spec=IMessageRepository)
        mock_sqlite_repo_class.return_value = mock_instance
        
        # Act
        from app.infrastructure.repository.message.sqlite_message_repository import SQLiteMessageRepository
        repo = SQLiteMessageRepository("dummy_path")
        
        # Assert
        assert repo == mock_instance
        mock_sqlite_repo_class.assert_called_once_with("dummy_path")

    def test_repository_exception_handling(self, mock_repository: Mock) -> None:
        """リポジトリで例外が発生した場合のテスト例"""
        # Arrange
        mock_repository.find_all.side_effect = Exception("データベース接続エラー")
        
        # Act & Assert
        with pytest.raises(Exception, match="データベース接続エラー"):
            mock_repository.find_all()