# uv run scripts/sample/sample.py
# /// script
# dependencies = [
#     "japanize-matplotlib",
#     "matplotlib",
#     "numpy",
#     "pandas",
# ]
# ///

# ruff: noqa: E402, F401  # import順を無視

"""コメント

export: インタラクティブ画面側の、エクスポート > HTMLから、Output込みのJupyter形式のファイルをHTMLとしてエクスポートできます
"""  # noqa

# %%[markdown]
# # H1

# %%
import sys

import japanize_matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import display

sys.path.append("/app")

from IPython import InteractiveShell

from app.di import get_injector
from app.domain.message.message import Message
from app.usecase.history import HistoryUsecase
from app.usecase.register import RegisterUsecase

np.set_printoptions(
    edgeitems=10,  # 省略表示する際の表示数
    suppress=True,  # 指数表示をしない
)
plt.rcParams["font.size"] = 14
InteractiveShell.ast_node_interactivity = "all"  # セル内の全ての出力を表示する

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
injector = get_injector()
register_usecase = injector.get(RegisterUsecase)
message = Message(content=text)
register_usecase.execute(message)

# %%
history_usecase = injector.get(HistoryUsecase)
messages = history_usecase.execute()
for m in messages:
    print(m.content)

# %%
