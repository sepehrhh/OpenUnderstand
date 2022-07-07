import os
import math
import sys
from antlr4 import *
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
        self.N1 = 0
        self.N2 = 0
        self.unique_operand = []
        self.unique_operator = []

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        self.N1 += 1
        self.N2 += 2
        if ctx.children[1].children[0].children[0].getText() not in self.unique_operand:
            self.unique_operand.append(ctx.children[1].children[0].children[0].getText())
        if ctx.children[1].children[0].children[1].getText() not in self.unique_operator:
            self.unique_operator.append(ctx.children[1].children[0].children[0].getText())

    def enterLocalVariableDeclaration(self, ctx: JavaParserLabeled.LocalVariableDeclarationContext):
        self.N1 += 1
        self.N2 += 2
        if ctx.children[1].children[0].children[0].getText() not in self.unique_operand:
            self.unique_operand.append(ctx.children[1].children[0].children[0].getText())
        if ctx.children[1].children[0].children[1].getText() not in self.unique_operator:
            self.unique_operator.append(ctx.children[1].children[0].children[0].getText())

    # ++ -- postfix
    def enterExpression6(self, ctx: JavaParserLabeled.Expression6Context):
        self.N1 += 1
        self.N2 += 1
        if ctx.children[0] not in self.unique_operand:
            self.unique_operand.append(ctx.children[0])
        if ctx.children[1] not in self.unique_operator:
            self.unique_operator.append(ctx.children[1])

    # ++ -- prefix
    def enterExpression7(self, ctx: JavaParserLabeled.Expression7Context):
        self.N1 += 1
        self.N2 += 1
        if ctx.children[1] not in self.unique_operand:
            self.unique_operand.append(ctx.children[1])
        if ctx.children[0] not in self.unique_operator:
            self.unique_operator.append(ctx.children[0])

    # ~ !
    def enterExpression8(self, ctx: JavaParserLabeled.Expression8Context):
        self.N1 += 1
        self.N2 += 1
        if ctx.children[1] not in self.unique_operand:
            self.unique_operand.append(ctx.children[1])
        if ctx.children[0] not in self.unique_operator:
            self.unique_operator.append(ctx.children[0])

    # * / %
    def enterExpression9(self, ctx: JavaParserLabeled.Expression9Context):
        self.N1 += 1
        self.N2 += 2
        self.check_expression(ctx)

    # + -
    def enterExpression10(self, ctx: JavaParserLabeled.Expression10Context):
        self.N1 += 1
        self.N2 += 2
        self.check_expression(ctx)

    # < > <= =>
    def enterExpression12(self, ctx: JavaParserLabeled.Expression12Context):
        self.N1 += 1
        self.N2 += 2
        self.check_expression(ctx)

    # == !+
    def enterExpression14(self, ctx: JavaParserLabeled.Expression14Context):
        self.N1 += 1
        self.N2 += 2
        self.check_expression(ctx)

    # &
    def enterExpression15(self, ctx: JavaParserLabeled.Expression15Context):
        self.N1 += 1
        self.N2 += 2
        self.check_expression(ctx)

    # ^
    def enterExpression16(self, ctx: JavaParserLabeled.Expression16Context):
        self.N1 += 1
        self.N2 += 2
        self.check_expression(ctx)

    # |
    def enterExpression17(self, ctx: JavaParserLabeled.Expression17Context):
        self.N1 += 1
        self.N2 += 2
        self.check_expression(ctx)

    # &&
    def enterExpression18(self, ctx: JavaParserLabeled.Expression18Context):
        self.N1 += 1
        self.N2 += 2
        self.check_expression(ctx)

    # ||
    def enterExpression19(self, ctx: JavaParserLabeled.Expression19Context):
        self.N1 += 1
        self.N2 += 2
        self.check_expression(ctx)

    # ?
    def enterExpression20(self, ctx: JavaParserLabeled.Expression20Context):
        self.N1 += 1
        self.N2 += 3
        if ctx.children[4] not in self.unique_operand:
            self.unique_operand.append(ctx.children[4])
        if ctx.children[2] not in self.unique_operand:
            self.unique_operand.append(ctx.children[2])
        if ctx.children[1] not in self.unique_operator:
            self.unique_operator.append(ctx.children[1])
        if ctx.children[3] not in self.unique_operator:
            self.unique_operator.append(ctx.children[3])

    # '=' | '+=' | '-=' | '*=' | '/=' | '&=' | '|=' | '^=' | '>>=' | '>>>=' | '<<=' | '%='
    def enterExpression21(self, ctx: JavaParserLabeled.Expression21Context):
        self.N1 += 1
        self.N2 += 2
        self.check_expression(ctx)

    def check_expression(self, ctx):
        if ctx.children[0] not in self.unique_operand:
            self.unique_operand.append(ctx.children[0])
        if ctx.children[2] not in self.unique_operand:
            self.unique_operand.append(ctx.children[2])
        if ctx.children[1] not in self.unique_operator:
            self.unique_operator.append(ctx.children[1])


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
            print(round(math.log(capital_n, 2) * n, 2))
        else:
            print(0)
        print('=' * 25)
