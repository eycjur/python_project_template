"""テストの前後の処理を記述

- srcディレクトリにパスを通す
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.absolute()))
