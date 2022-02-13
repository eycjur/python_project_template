"""テストの前後の処理を記述

- python_project_templateディレクトリにパスを通す
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.joinpath("python_project_template")))
