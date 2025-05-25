"""共通のDIコンテナファクトリーを提供する"""

from functools import lru_cache
from typing import Optional

from injector import Injector

from app.di import get_di_module
from app.settings import RunEnv


@lru_cache(maxsize=1)
def get_shared_injector(cloud: Optional[RunEnv] = None) -> Injector:
    """共有のDIコンテナを取得する
    
    このファクトリーは全ての presentation layer で使用され、
    一貫した依存性注入パターンを提供する。
    
    Args:
        cloud: 実行環境（省略時は設定から自動判定）
        
    Returns:
        Injector: 設定済みのDIコンテナ
    """
    return Injector(get_di_module(cloud))


def create_injector(cloud: Optional[RunEnv] = None) -> Injector:
    """新しいDIコンテナを作成する
    
    テスト時など、独立したコンテナが必要な場合に使用する。
    通常は get_shared_injector() を使用すること。
    
    Args:
        cloud: 実行環境（省略時は設定から自動判定）
        
    Returns:
        Injector: 新しいDIコンテナ
    """
    return Injector(get_di_module(cloud))