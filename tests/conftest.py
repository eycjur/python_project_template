"""テストの前後の処理を記述

- appディレクトリにパスを通す
- 各テスト前にDIコンテナをリセット
"""

import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parent.parent.absolute()))


@pytest.fixture(autouse=True)
def reset_di_container() -> None:
    """各テスト前にグローバルなDIコンテナをリセットする"""
    from app.di import reset_injector

    reset_injector()
