# ruff: noqa: E402, F401  # import順を無視

"""コメント"""

# %%[markdown]
# # H1

# %%
import sys

sys.path.append("/app")

from src.settings import *  # noqa

# %autoreload 2
# %load_ext autoreload

# %%
print("Hello, world!")
