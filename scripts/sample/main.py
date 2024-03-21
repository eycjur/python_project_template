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
