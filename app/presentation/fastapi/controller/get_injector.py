from injector import Injector

from app.shared.injector_factory import get_shared_injector


def get_injector() -> Injector:
    """FastAPI用のDIコンテナを取得する
    
    共有インスタンスを使用してパフォーマンスを向上させる。
    """
    return get_shared_injector()
