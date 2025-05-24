"""パラメータ化テストの例テンプレート

このファイルは、pytest.mark.parametrizeを使用したパラメータ化テストの例です。
実際のテストでは、このファイルから必要なパターンをコピーして使用してください。
"""

import pytest
from fastapi.testclient import TestClient

from app.domain.message.message import Message


class TestParametrizedExamples:
    """パラメータ化テストの例を示すクラス"""

    # ========================================
    # 基本的なパラメータ化テスト
    # ========================================

    @pytest.mark.parametrize("content", [
        "通常のメッセージ",
        "",
        "特殊文字!@#$%^&*()",
        "改行\nありメッセージ",
        "Unicode絵文字😀🎉",
        "長いメッセージ" + "あ" * 100,
    ])
    def test_message_creation_with_various_content(self, content: str) -> None:
        """様々なコンテンツでのMessage作成テスト"""
        # Act
        message = Message(content)
        
        # Assert
        assert message.content == content

    @pytest.mark.parametrize("limit", [1, 5, 10, 50, 100])
    def test_message_limit_parameter(self, limit: int) -> None:
        """様々なlimit値のテスト"""
        # このテストは実際の実装に合わせて調整してください
        assert limit > 0

    # ========================================
    # 複数パラメータの組み合わせ
    # ========================================

    @pytest.mark.parametrize("content,expected_length", [
        ("短い", 2),
        ("もう少し長いメッセージ", 9),
        ("", 0),
        ("a" * 1000, 1000),
    ])
    def test_message_content_length(self, content: str, expected_length: int) -> None:
        """メッセージ内容と期待される長さのテスト"""
        # Act
        message = Message(content)
        
        # Assert
        assert len(message.content) == expected_length

    @pytest.mark.parametrize("content,should_be_empty", [
        ("テストメッセージ", False),
        ("", True),
        ("   ", False),  # 空白文字は空とは扱わない
        ("\n", False),   # 改行文字は空とは扱わない
    ])
    def test_message_empty_check(self, content: str, should_be_empty: bool) -> None:
        """メッセージの空判定テスト"""
        # Act
        message = Message(content)
        is_empty = len(message.content) == 0
        
        # Assert
        assert is_empty == should_be_empty

    # ========================================
    # 例外ケースのパラメータ化
    # ========================================

    @pytest.mark.parametrize("invalid_input,expected_exception", [
        (None, TypeError),
        (123, TypeError),
        (["list"], TypeError),
        ({"dict": "value"}, TypeError),
    ])
    def test_message_creation_with_invalid_input(
        self, 
        invalid_input: any, 
        expected_exception: type
    ) -> None:
        """無効な入力でのMessage作成テスト"""
        # Act & Assert
        with pytest.raises(expected_exception):
            Message(invalid_input)

    # ========================================
    # HTTPレスポンスのパラメータ化テスト
    # ========================================

    @pytest.mark.parametrize("message_content,expected_status", [
        ("正常なメッセージ", 200),
        ("", 200),  # 空文字も許可する場合
        ("特殊文字!@#", 200),
        ("長いメッセージ" + "あ" * 1000, 200),
    ])
    def test_post_message_various_content(
        self, 
        test_client: TestClient, 
        message_content: str, 
        expected_status: int
    ) -> None:
        """様々なメッセージ内容でのPOSTテスト
        
        注意: test_clientフィクスチャが必要です
        """
        # Act
        response = test_client.post("/messages", json={"content": message_content})
        
        # Assert
        assert response.status_code == expected_status

    # ========================================
    # IDを使用したパラメータ化（テスト名の明確化）
    # ========================================

    @pytest.mark.parametrize("content", [
        pytest.param("", id="empty_string"),
        pytest.param("通常のメッセージ", id="normal_message"),
        pytest.param("特殊文字!@#$%", id="special_characters"),
        pytest.param("改行\nあり", id="with_newline"),
        pytest.param("長い" + "メッセージ" * 100, id="long_message"),
    ])
    def test_message_with_named_parameters(self, content: str) -> None:
        """名前付きパラメータでのテスト（テスト名が明確になる）"""
        # Act
        message = Message(content)
        
        # Assert
        assert message.content == content

    # ========================================
    # 条件付きスキップを含むパラメータ化
    # ========================================

    @pytest.mark.parametrize("content", [
        "通常のメッセージ",
        pytest.param(
            "長いメッセージ" + "あ" * 10000, 
            marks=pytest.mark.skip(reason="メモリ使用量が大きいため一時的にスキップ")
        ),
        "短いメッセージ",
    ])
    def test_message_with_conditional_skip(self, content: str) -> None:
        """条件付きスキップを含むパラメータ化テスト"""
        # Act
        message = Message(content)
        
        # Assert
        assert message.content == content

    # ========================================
    # フィクスチャとパラメータの組み合わせ
    # ========================================

    @pytest.fixture(params=["repo1", "repo2", "repo3"])
    def repository_type(self, request: pytest.FixtureRequest) -> str:
        """リポジトリタイプのフィクスチャ"""
        return request.param

    @pytest.mark.parametrize("message_count", [1, 5, 10])
    def test_repository_with_various_message_counts(
        self, 
        repository_type: str, 
        message_count: int
    ) -> None:
        """リポジトリタイプとメッセージ数の組み合わせテスト"""
        # このテストは実際の実装に合わせて調整してください
        assert repository_type in ["repo1", "repo2", "repo3"]
        assert message_count > 0

    # ========================================
    # 複雑なテストデータのパラメータ化
    # ========================================

    @pytest.mark.parametrize("test_case", [
        {
            "name": "正常ケース",
            "input": {"content": "テストメッセージ"},
            "expected_status": 200,
            "expected_response_keys": ["id", "content", "created_at"],
        },
        {
            "name": "空文字ケース", 
            "input": {"content": ""},
            "expected_status": 200,
            "expected_response_keys": ["id", "content", "created_at"],
        },
        {
            "name": "長文ケース",
            "input": {"content": "長いメッセージ" * 100},
            "expected_status": 200,
            "expected_response_keys": ["id", "content", "created_at"],
        },
    ])
    def test_complex_test_cases(
        self, 
        test_client: TestClient, 
        test_case: dict
    ) -> None:
        """複雑なテストケースのパラメータ化テスト
        
        注意: test_clientフィクスチャが必要です
        """
        # Act
        response = test_client.post("/messages", json=test_case["input"])
        
        # Assert
        assert response.status_code == test_case["expected_status"]
        
        if response.status_code == 200:
            response_data = response.json()
            for key in test_case["expected_response_keys"]:
                assert key in response_data