import ast
import objects
import tokens


class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self._table = {}

    def get(self, ident):
        try:
            return self._table[ident.literal]
        except KeyError:
            if self.parent is None:
                raise ValueError(f"Unbound variable `{ident.literal}`")

            return self.parent.get(ident)

    def set(self, ident, value):
        self._table[ident.literal] = value


class Evaluator:

    def eval(self, ast_node, env):
        if isinstance(ast_node, ast.Assignment):
            return self.eval_assignment(ast_node, env)
        if isinstance(ast_node, ast.Return):
            return self.eval_return(ast_node, env)
        if isinstance(ast_node, ast.Conditional):
            return self.eval_conditional(ast_node, env)
        if isinstance(ast_node, ast.Block):
            return self.eval_block(ast_node, env)
        if isinstance(ast_node, ast.Expression):
            return self.eval_expression(ast_node, env)
        else:
            pass

    def eval_program(self, program):
        env = Environment()
        for statement in program.statements:
            return_ = self.eval(statement, env)

        return return_

    def eval_assignment(self, ast_node, env):
        ident = ast_node.ident
        value = self.eval(ast_node.expr, env)
        env.set(ident, value)

    def eval_return(self, ast_node, env):
        value = self.eval(ast_node.expr, env)

        return objects.Returned(value)

    def eval_conditional(self, ast_node, env):
        condition = self.eval(ast_node.cond, env)
        if condition == objects.TRUE:
            return self.eval(ast_node.cons, env)
        elif ast_node.alt is not None:
            return self.eval(ast_node.alt, env)

    def eval_block(self, ast_node, env):
        for stmt in ast_node.statements:
            last = self.eval(stmt, env)
            if isinstance(last, objects.Returned):
                return last.obj

        return last

    def eval_expression(self, ast_node, env):
        if isinstance(ast_node, ast.Identifier):
            return self.eval_identifier(ast_node, env)
        if isinstance(ast_node, ast.IntLiteral):
            return self.eval_int_literal(ast_node, env)
        if isinstance(ast_node, ast.BoolLiteral):
            return self.eval_bool_literal(ast_node, env)
        if isinstance(ast_node, ast.StringLiteral):
            return self.eval_string_literal(ast_node, env)

        if isinstance(ast_node, ast.BinaryOp):
            return self.eval_binary_op(ast_node, env)
        if isinstance(ast_node, ast.PrefixOp):
            return self.eval_prefix_op(ast_node, env)

        if isinstance(ast_node, ast.FunctionLiteral):
            return self.eval_func_literal(ast_node, env)
        if isinstance(ast_node, ast.FunctionCall):
            return self.eval_func_call(ast_node, env)
        else:
            raise ValueError(
                f"Expression of type {ast_node} cannot be evaluated")

    def eval_identifier(self, ast_node, env):
        return env.get(ast_node.ident)

    def eval_int_literal(self, ast_node, env):
        value = int(ast_node.literal)

        return objects.Integer(value)

    def eval_bool_literal(self, ast_node, env):
        if ast_node.literal == 'true':
            return objects.TRUE

        return objects.FALSE

    def eval_string_literal(self, ast_node, env):
        value = str(ast_node.literal)

        return objects.String(value)

    def eval_prefix_op(self, ast_node, env):
        op = ast_node.op
        right = self.eval_expression(ast_node.right, env)
        if isinstance(op, tokens.MINUS):
            return objects.Integer(-right)

    def eval_binary_op(self, ast_node, env):
        op = ast_node.op
        # left = self.eval_expression(ast_node.left, env)
        left = self.eval(ast_node.left, env)
        # right = self.eval_expression(ast_node.right, env)
        right = self.eval(ast_node.right, env)
        if isinstance(op, tokens.PLUS):
            return objects.Integer(left + right)
        if isinstance(op, tokens.MINUS):
            return objects.Integer(left - right)
        if isinstance(op, tokens.ASTERISK):
            return objects.Integer(left * right)
        if isinstance(op, tokens.SLASH):
            return objects.Integer(left / right)
        if isinstance(op, tokens.EQ):
            if left == right:
                return objects.TRUE
            return objects.FALSE
        if isinstance(op, tokens.NEQ):
            if left != right:
                return objects.TRUE
            return objects.FALSE
        if isinstance(op, tokens.GT):
            if left > right:
                return objects.TRUE
            return objects.FALSE
        if isinstance(op, tokens.LT):
            if left < right:
                return objects.TRUE
            return objects.FALSE
        if isinstance(op, tokens.GTE):
            if left >= right:
                return objects.TRUE
            return objects.FALSE
        if isinstance(op, tokens.LTE):
            if left <= right:
                return objects.TRUE
            return objects.FALSE

    def eval_func_literal(self, ast_node, env):
        params = ast_node.params
        body = ast_node.body
        name = ast_node.name

        func = objects.Function(params, body)

        if name is not None:
            env.set(name, func)

        return func

    def eval_func_call(self, ast_node, env):
        func = self.eval(ast_node.ident, env)
        args = ast_node.args

        return self.eval_func(func, args, env)

    def eval_func(self, func, args, env):
        local_env = Environment(parent=env)
        params = func.params
        body = func.body

        if len(args) != len(params):
            raise ValueError(
                f"Number of arguments passed {len(args)} != number of parameters {len(params)}")

        for param, arg in zip(params, args):
            local_env.set(param, self.eval_expression(arg, local_env))

        return self.eval_block(body, local_env)


def eval_file(file_):
    from parser import parse_source

    with open(file_) as f:
        source = f.read()

    ast_node = parse_source(source)

    evaluator = Evaluator()
    # The print will be avoided after implementation of print in the language
    print(evaluator.eval_program(ast_node))
