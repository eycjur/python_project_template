"""テストユーティリティ関数のテンプレート

このファイルは、テストで頻繁に使用されるユーティリティ関数のテンプレートです。
実際のテストでは、このファイルから必要な関数をコピーして使用してください。
"""

from typing import Any, Callable, Type
from unittest.mock import Mock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.domain.message.message import Message


# ========================================
# アサーション関連のユーティリティ
# ========================================

def assert_message_equal(actual: Message, expected: Message) -> None:
    """Messageオブジェクトの内容が等しいかを検証
    
    Args:
        actual: 実際のMessage
        expected: 期待されるMessage
    """
    assert actual.content == expected.content
    assert actual.created_at == expected.created_at


def assert_message_list_equal(actual: list[Message], expected: list[Message]) -> None:
    """Messageリストの内容が等しいかを検証
    
    Args:
        actual: 実際のMessageリスト
        expected: 期待されるMessageリスト
    """
    assert len(actual) == len(expected)
    for actual_msg, expected_msg in zip(actual, expected):
        assert_message_equal(actual_msg, expected_msg)


def assert_mock_called_with_message_content(mock: Mock, expected_content: str) -> None:
    """モックが指定したコンテンツのMessageで呼ばれたかを検証
    
    Args:
        mock: 検証対象のモック
        expected_content: 期待されるメッセージ内容
    """
    mock.assert_called_once()
    called_message = mock.call_args[0][0]
    assert isinstance(called_message, Message)
    assert called_message.content == expected_content


# ========================================
# テストデータ生成関連のユーティリティ
# ========================================

def create_test_message(content: str = "テストメッセージ") -> Message:
    """テスト用のMessageを作成
    
    Args:
        content: メッセージ内容（デフォルト: "テストメッセージ"）
        
    Returns:
        Message: テスト用Message
    """
    return Message(content)


def create_test_messages(count: int, prefix: str = "メッセージ") -> list[Message]:
    """指定した数のテスト用Messageリストを作成
    
    Args:
        count: 作成するメッセージ数
        prefix: メッセージ内容のプレフィックス
        
    Returns:
        list[Message]: テスト用Messageリスト
    """
    return [Message(f"{prefix}{i+1}") for i in range(count)]


def create_long_content_message(length: int = 1000) -> Message:
    """指定した長さのコンテンツを持つテスト用Messageを作成
    
    Args:
        length: コンテンツの長さ
        
    Returns:
        Message: 長いコンテンツを持つテスト用Message
    """
    content = "あ" * length
    return Message(content)


# ========================================
# HTTP関連のユーティリティ
# ========================================

def assert_http_success(response: Any) -> None:
    """HTTPレスポンスが成功ステータスかを検証
    
    Args:
        response: HTTPレスポンス
    """
    assert response.status_code == status.HTTP_200_OK


def assert_http_created(response: Any) -> None:
    """HTTPレスポンスが作成ステータスかを検証
    
    Args:
        response: HTTPレスポンス
    """
    assert response.status_code == status.HTTP_201_CREATED


def assert_http_bad_request(response: Any) -> None:
    """HTTPレスポンスがバッドリクエストステータスかを検証
    
    Args:
        response: HTTPレスポンス
    """
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def post_message_and_assert_success(
    client: TestClient, 
    content: str = "テストメッセージ"
) -> Any:
    """メッセージをPOSTして成功を検証
    
    Args:
        client: FastAPIテストクライアント
        content: メッセージ内容
        
    Returns:
        HTTPレスポンス
    """
    response = client.post("/messages", json={"content": content})
    assert_http_success(response)
    return response


def get_messages_and_assert_success(client: TestClient) -> Any:
    """メッセージリストをGETして成功を検証
    
    Args:
        client: FastAPIテストクライアント
        
    Returns:
        HTTPレスポンス
    """
    response = client.get("/messages")
    assert_http_success(response)
    return response


# ========================================
# 例外テスト関連のユーティリティ
# ========================================

def assert_raises_with_message(
    exception_type: Type[Exception], 
    expected_message: str, 
    callable_func: Callable[[], Any],
    *args: Any,
    **kwargs: Any
) -> None:
    """指定した例外とメッセージが発生することを検証
    
    Args:
        exception_type: 期待される例外のタイプ
        expected_message: 期待される例外メッセージ
        callable_func: 実行する関数
        *args: 関数の引数
        **kwargs: 関数のキーワード引数
    """
    with pytest.raises(exception_type, match=expected_message):
        callable_func(*args, **kwargs)


def setup_mock_to_raise_exception(
    mock: Mock, 
    method_name: str, 
    exception: Exception
) -> None:
    """モックの指定したメソッドが例外を発生するように設定
    
    Args:
        mock: 設定対象のモック
        method_name: メソッド名
        exception: 発生させる例外
    """
    getattr(mock, method_name).side_effect = exception


# ========================================
# パフォーマンステスト関連のユーティリティ
# ========================================

def measure_execution_time(func: Callable[[], Any]) -> tuple[Any, float]:
    """関数の実行時間を測定
    
    Args:
        func: 実行時間を測定する関数
        
    Returns:
        tuple[Any, float]: (関数の戻り値, 実行時間（秒）)
    """
    import time
    
    start_time = time.time()
    result = func()
    end_time = time.time()
    execution_time = end_time - start_time
    
    return result, execution_time


def assert_execution_time_under(
    func: Callable[[], Any], 
    max_seconds: float
) -> Any:
    """関数の実行時間が指定した秒数以下であることを検証
    
    Args:
        func: 実行時間を測定する関数
        max_seconds: 最大実行時間（秒）
        
    Returns:
        関数の戻り値
    """
    result, execution_time = measure_execution_time(func)
    assert execution_time <= max_seconds, f"実行時間が{max_seconds}秒を超えました: {execution_time}秒"
    return result


# ========================================
# テスト環境セットアップ関連のユーティリティ
# ========================================

def reset_mock_calls(mock: Mock) -> None:
    """モックの呼び出し履歴をリセット
    
    Args:
        mock: リセット対象のモック
    """
    mock.reset_mock()


def configure_mock_repository_with_data(
    mock: Mock, 
    messages: list[Message]
) -> None:
    """モックリポジトリにテストデータを設定
    
    Args:
        mock: 設定対象のモックリポジトリ
        messages: 設定するメッセージリスト
    """
    mock.find_all.return_value = messages


def create_isolated_test_environment() -> dict[str, Any]:
    """分離されたテスト環境を作成
    
    Returns:
        dict[str, Any]: テスト環境の設定情報
    """
    return {
        "db_path": ":memory:",
        "log_level": "DEBUG",
        "test_mode": True,
    }