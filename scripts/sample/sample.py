# ruff: noqa: E402, F401  # import順を無視

"""コメント"""  # noqa

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

from src.domain.message.message import Message
from src.init import get_message_repository
from src.usecase.history import HistoryUsecase
from src.usecase.register import RegisterUsecase

np.set_printoptions(
    edgeitems=3,  # 表示する要素数の最大
    suppress=True,  # 指数表示をしない
)
plt.rcParams["font.size"] = 14

#!%load_ext autoreload
#!%autoreload 2

# %%
text = "こんにちは"

# %%
message_repository = get_message_repository()
message = Message(content=text)
RegisterUsecase(message_repository).execute(message)

# %%
#!%%time
message_repository = get_message_repository()
messages = HistoryUsecase(message_repository).execute()
for m in messages:
    print(m.content)

# %%
