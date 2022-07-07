from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
import analysis_passes.class_properties as class_properties


class CallAndCallBy(JavaParserLabeledListener):
    implement = []

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        bodies = ctx.classBody().classBodyDeclaration()
        if bodies is not None:
            for body in bodies:
                member = getattr(body, 'memberDeclaration', None)
                if member is not None:
                    member = member()
                    method = getattr(member, 'methodDeclaration', None)
                    if method is not None:
                        method = method()
                        block = method.methodBody().block()
                        self.dfs(block, method, ctx)

    def dfs(self, ctx, cls, context):
        b_statements = ctx.blockStatement()
        for bStatement in b_statements:
            kk = str(type(bStatement)).split('.')[-1][:-2]
            kk2 = "BlockStatement1Context"
            if kk == kk2:
                statement = bStatement.statement()
                s = getattr(statement, 'statement', None)
                if s is not None:
                    s = s()
                    bb = getattr(s, 'block', None)
                    if bb is not None:
                        bb = bb()
                        self.dfs(bb, cls, context)
                else:
                    exp = getattr(statement, 'expression', None)
                    if exp is not None:
                        exp = exp()
                        exp2 = getattr(exp, 'expression', None)
                        if exp2 is not None:
                            exp2 = exp2()
                            primary = getattr(exp2, 'primary', None)
                            if primary is not None:
                                primary = primary()
                                super_var = getattr(primary, 'SUPER', None)
                                if super_var is not None:
                                    return
                        if type(exp) == list:
                            for exp3 in exp:
                                method_call = getattr(exp3, 'methodCall', None)
                                if method_call is not None:
                                    method_call = method_call()
                                    if method_call is not None:
                                        called = method_call.IDENTIFIER()
                                        scope_parents = class_properties.ClassPropertiesListener.findParents(context)
                                        if len(scope_parents) == 1:
                                            scope_longname = scope_parents[0]
                                        else:
                                            scope_longname = ".".join(scope_parents)
                                        line = context.children[0].symbol.line
                                        col = context.children[0].symbol.column
                                        self.implement.append(
                                            {"scope_kind": "Class", "scope_name": cls.IDENTIFIER().__str__(),
                                             "scope_longname": str(scope_longname),
                                             "scope_parent": scope_parents[-2] if len(scope_parents) > 2 else None,
                                             "scope_contents": cls.getText(),
                                             "scope_modifiers":
                                                 class_properties.ClassPropertiesListener.findClassOrInterfaceModifiers(
                                                     context),
                                             "line": line,
                                             "col": col,
                                             "type_ent_longname": str(called)})
                        else:
                            method_call = getattr(exp, 'methodCall', None)
                            if method_call is not None:
                                method_call = method_call()
                                if method_call is not None:
                                    called = method_call.IDENTIFIER()
                                    scope_parents = class_properties.ClassPropertiesListener.findParents(context)
                                    if len(scope_parents) == 1:
                                        scope_longname = scope_parents[0]
                                    else:
                                        scope_longname = ".".join(scope_parents)
                                    line = method_call.start.line
                                    col = method_call.start.column
                                    self.implement.append(
                                        {"scope_kind": "Class", "scope_name": cls.IDENTIFIER().__str__(),
                                         "scope_longname": str(scope_longname),
                                         "scope_parent": scope_parents[-2] if len(scope_parents) > 2 else None,
                                         "scope_contents": cls.getText(),
                                         "scope_modifiers":
                                             class_properties.ClassPropertiesListener.findClassOrInterfaceModifiers(
                                                 context),
                                         "line": line,
                                         "col": col,
                                         "type_ent_longname": str(called)})
