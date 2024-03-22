from src.domain.message.message import Message


def test_message_encode_decode_ok() -> None:
    """Messageが正しくエンコード、デコードできることを確認する。"""
    message = Message("content")

    encoded = message.to_repository()
    decoded = Message.from_repository(encoded)

    assert message == decoded
