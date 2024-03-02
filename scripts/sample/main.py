# ruff: noqa: E402, F401  # import順を無視

"""コメント

推奨設定
```json:settings.json
{
  // コードセルの解析時にシェル割り当て(#!)、行マジック(#!%)およびセルマジック(#!%%)のコメントを解除します。
  "jupyter.interactiveWindow.textEditor.magicCommandsAsComments": true,
  // デバッグするときにライブラリコードにステップインできるようにする。
  "jupyter.debugJustMyCode": false,
}
```
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

# display

sys.path.append("/app")

from src.usecase.sample import func

np.set_printoptions(
    edgeitems=3,  # 表示する要素数の最大
    suppress=True,  # 指数表示をしない
)
plt.rcParams["font.size"] = 14

#!%load_ext autoreload
#!%autoreload 2

# %%
print(func("Hello, world!"))

# %%
