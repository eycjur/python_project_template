# ruff: noqa: E402, F401  # import順を無視
#
# https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies
# /// script
# requires-python = "==3.12"
# dependencies = [
#     "numpy",
#     "pandas",
#     "matplotlib",
#     "japanize-matplotlib",
#     "ipython",
# ]
# ///

"""
# pythonで実行する
python scripts/sample/sample.py

# uvでstandaloneスクリプトとして実行する
uv run scripts/sample/sample.py

Tips:
- インタラクティブ画面側の、エクスポート > Jupyter形式のファイルをHTMLとしてエクスポートできます
"""  # noqa


# %%[markdown]
# # H1

# %%
import sys

import japanize_matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from injector import Injector

sys.path.append("/app")

from app.di import get_di_module
from app.domain.message.message import Message
from app.usecase.history import HistoryUsecase
from app.usecase.register import RegisterUsecase

np.set_printoptions(
    edgeitems=3,  # 表示する要素数の最大
    suppress=True,  # 指数表示をしない
)
plt.rcParams["font.size"] = 14

try:
    from IPython import InteractiveShell
    from IPython.display import display

    # セル内の全ての出力を表示する
    InteractiveShell.ast_node_interactivity = "all"  # type: ignore
except ModuleNotFoundError:
    print("Running in a non-interactive environment")

#!%load_ext autoreload
#!%autoreload 2
# エラー時に引数も表示する
#!%xmode Verbose

# %%
# 有用なマジックコマンド一覧(先頭の#を除いて利用して利用してください)
# #!%%time  # セルの実行時間を計測
# #!%load_ext line_profiler
# #!%lprun  # ラインプロファイリング

# %%
text = "こんにちは"

# %%
injector = Injector([get_di_module()])
register_usecase = injector.get(RegisterUsecase)
message = Message(content=text)
register_usecase.execute(message)

# %%
history_usecase = injector.get(HistoryUsecase)
messages = history_usecase.execute()
for m in messages:
    print(m.content)

# %%
