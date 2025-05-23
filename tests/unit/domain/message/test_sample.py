import pytest

from app.domain.message.message import Message


@pytest.mark.parametrize(
    "message",
    [
        # 普通のメッセージ
        Message("content"),
        # メッセージが空文字の場合
        Message(""),
    ],
    ids=["normal_message", "empty_message"],
)
def test_message_encode_decode_ok(message: Message) -> None:
    """Messageが正しくエンコード、デコードできることを確認する。"""
    encoded = message.to_repository()
    decoded = Message.from_repository(encoded)

    assert message == decoded
