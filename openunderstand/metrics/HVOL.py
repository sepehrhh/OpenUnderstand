import os
import sys
from antlr4 import *
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


PRJ_INDEX = 0


def get_project_info(index):
    project_names = [
        'calculator_app',
        'JSON',
        'testing_legacy_code',
        'jhotdraw-develop',
        'xerces2j',
        'jvlt-1.3.2',
        'jfreechart',
        'ganttproject',
        '105_freemind',
    ]
    project_name = project_names[index]
    project_path = f"../../../benchmarks/{project_name}"
    print(project_path)
    project_path = os.path.abspath(project_path)

    return {
        'PROJECT_NAME': project_name,
        'PROJECT_PATH': project_path,
    }


def get_parse_tree(path):
    file = FileStream(path, encoding="utf-8")
    lexer = JavaLexer(file)
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    return parser.compilationUnit()


class Project:
    def __init__(self, project_dir, project_name=None):
        self.project_dir = project_dir
        self.project_name = project_name
        self.files = []

    def get_java_files(self):
        for dir_path, _, file_names in os.walk(self.project_dir):
            for file in file_names:
                if '.java' in str(file):
                    path = os.path.join(dir_path, file)
                    path = path.replace("/", "\\")
                    path = os.path.abspath(path)
                    self.files.append((file, path))


class HVOLListener(JavaParserLabeledListener):
    def __init__(self, files):
        self.repository = {}
        self.files = files
        self.counter = 0

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        print(ctx.children)


if __name__ == '__main__':
    info = get_project_info(PRJ_INDEX)
    print(info['PROJECT_PATH'])
    print(info['PROJECT_NAME'])
    p = Project(info['PROJECT_PATH'], info['PROJECT_NAME'])
    p.get_java_files()
    # print(11111)
    for file_name, file_path in p.files:
        # print(file_name)
        print(file_path)
        tree = get_parse_tree(file_path)
        listener = HVOLListener(p.files)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
