from src.usecase.sample import func


def test_func() -> None:
    assert func("hello") == "あなたの入力はhelloです"
