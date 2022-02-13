from add.add import add
from conf.conf import CFG
from utils import settings

if __name__ == "__main__":
    print(CFG.is_debug_mode)
    print(add(3, 5))
    settings.pass_func()
