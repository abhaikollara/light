
class Statement:
    pass


class Expression:
    pass


class Program():
    def __init__(self, statements):
        self.statements = statements
    
    def __getitem__(self, idx):
        return self.statements[idx]


class Block(Statement):
    def __init__(self, statements):
        self.statements = statements


class Assignment(Statement):
    def __init__(self, ident, expr):
        self.ident = ident
        self.expr = expr

    def __repr__(self):
        return f"Assignment({repr(self.ident)}, {repr(self.expr)})"


class Return(Statement):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"Return({repr(self.expr)})"


class Conditional(Statement):
    def __init__(self, cond, cons, alt=None):
        self.cond = cond
        self.cons = cons
        self.alt = alt


class Identifier(Expression):
    def __init__(self, ident):
        self.ident = ident
        self.literal = ident.literal

    def __repr__(self):
        return f"Identifier({self.literal})"

class FunctionLiteral(Expression):
    def __init__(self, params, body, name=None):
        self.params = params
        self.body = body
        self.name = name

    def __repr__(self):
        return f"FunctionLiteral({repr(self.name)}, {repr(self.params)})"


class FunctionCall(Expression):
    def __init__(self, ident, args):
        self.ident = ident
        self.name = self.ident.literal
        self.args = args

    def __repr__(self):
        return f"FunctionCall({repr(self.name)}, {repr(self.args)})"


class IntLiteral(Expression):
    def __init__(self, token):
        self.token = token
        self.literal = self.token.literal

    def __repr__(self):
        return f"IntLiteral({repr(self.literal)})"


class BoolLiteral(Expression):
    def __init__(self, token):
        self.token = token
        self.literal = self.token.literal

    def __repr__(self):
        return f"BoolLiteral({repr(self.literal)})"


class StringLiteral(Expression):
    def __init__(self, literal):
        self.token = token
        self.literal = self.token.literal

    def __repr__(self):
        return f"StringLiteral({repr(self.literal)})"


class BinaryOp(Expression):
    def __init__(self, op, left, right):
        self.left = left
        self.right = right
        self.op = op
    
    def __repr__(self):
        return f"BinaryOp({self.left}, {self.op},  {self.right})"


class PrefixOp(Expression):
    def __init__(self, op, right):
        self.op = op
        self.right = right
