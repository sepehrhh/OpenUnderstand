import math
from antlr4 import *
from HVOL import get_project_info, get_parse_tree, Project, HVOLListener


PRJ_INDEX = 0


if __name__ == '__main__':
    info = get_project_info(PRJ_INDEX)
    print(info['PROJECT_PATH'])
    print(info['PROJECT_NAME'])
    p = Project(info['PROJECT_PATH'], info['PROJECT_NAME'])
    p.get_java_files()
    for file_name, file_path in p.files:
        tree = get_parse_tree(file_path)
        listener = HVOLListener(p.files)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        n = len(listener.unique_operator) + len(listener.unique_operand)
        capital_n = listener.N1 + listener.N2
        print(file_name)
        print(file_path)
        if capital_n > 0:
            v = math.log(capital_n, 2) * n
        else:
            v = 0
        if listener.N2 > 0:
            d = (len(listener.unique_operator) / 2) * (listener.N2 / len(listener.unique_operand))
        else:
            d = 0
        print(round(d * v, 2))
        print('=' * 25)
