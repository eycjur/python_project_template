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

from injector import Injector

from src.di import get_di_module
from src.domain.message.message import Message
from src.usecase.history import HistoryUsecase
from src.usecase.register import RegisterUsecase

np.set_printoptions(
    edgeitems=3,  # 表示する要素数の最大
    suppress=True,  # 指数表示をしない
)
plt.rcParams["font.size"] = 14

#!%load_ext autoreload
#!%autoreload 2
# エラー時に引数も表示する
#!%xmode Verbose

# %%
# 有用なマジックコマンド一覧（先頭の#を除いて利用して利用してください）
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
