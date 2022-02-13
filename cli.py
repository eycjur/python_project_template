from python_project_template.add.add import add
from python_project_template.conf.conf import CFG

if __name__ == "__main__":
    print(CFG.is_debug_mode)
    print(add(3, 5))
