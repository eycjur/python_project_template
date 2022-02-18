# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: 'Python 3.10.1 (''.venv'': poetry)'
#     language: python
#     name: python3
# ---

# %%
import sys; sys.path.append("..")

import japanize_matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.config import settings

np.set_printoptions(edgeitems=3)
plt.rcParams["font.size"] = 14
# %matplotlib inline
# %precision 3

# %load_ext autoreload
# %autoreload 2
# %load_ext line_profiler

# %%
