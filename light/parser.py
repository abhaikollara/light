import ast
import tokens

class ParserError(Exception): pass


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.tokens = tokens

    @property
    def current(self):
        try:
            return self.tokens[self.position]
        except IndexError:
            raise ParserError("Reached EOF while parsing")

    @property
    def next(self):
        try:
            return self.tokens[self.position+1]
        except IndexError:
            raise ParserError("Reached EOF while parsing")

    def step(self, n=1):
        self.position += n

    def step_back(self, n=1):
        self.position -= n

    def read_char(self, n=1):
        self.position += n
        return self.current

    def parse_program(self):
        statements = []
        while not isinstance(self.current, tokens.EOF):
            if isinstance(self.current, tokens.SEMICOLON):
                self.step()
                continue
            if isinstance(self.current, tokens.LET):
                stmt = self.parse_let()
            elif isinstance(self.current, tokens.FUNC):
                stmt = self.parse_function_literal()
            elif isinstance(self.current, tokens.RETURN):
                stmt = self.parse_return()
            elif isinstance(self.current, tokens.IF):
                stmt = self.parse_conditional()
            elif isinstance(self.current, tokens.LBRACE):
                stmt = self.parse_block()
            else:
                stmt = self.parse_expr()

            statements.append(stmt)

        return ast.Program(statements)

    def parse_let(self):
        tok = self.current
        self.step()
        if not isinstance(self.current, tokens.IDENT):
            raise ParserError(f"Expected identifer after `let` keyword, found {self.current}")
        ident = self.parse_identifier()

        if not isinstance(self.current, tokens.ASSIGN):
            raise ParserError(f"Expected `=` after identifier keyword, found {self.current}")
        
        self.step()
        expr = self.parse_expr()

        return ast.Assignment(ident, expr)
        

    def parse_return(self):
        self.step()
        expr = self.parse_expr()

        return ast.Return(expr)

    def parse_conditional(self):
        #Check for IF token
        self.step()
        cond = self.parse_expr()
        cons = self.parse_block()
        alt = None
        if isinstance(self.current, tokens.ELSE):
            self.step()
            alt = self.parse_block()
        
        return ast.Conditional(cond, cons, alt)

    def parse_identifier(self):
        ident = self.current
        self.step()
        return ast.Identifier(ident)

    def parse_function_call(self):
        ident = self.parse_identifier()

        if not isinstance(self.current, tokens.LPARAN):
            raise ParserError(f"Expected `(` after function name, found {self.current}")
        
        if isinstance(self.read_char(), tokens.RPARAN):
            return ast.FunctionCall(ident, [])

        args = []
        while True:
            if isinstance(self.current, tokens.RPARAN):
                break
            args.append(self.parse_expr())

            if isinstance(self.current, tokens.COMMA):
                self.step()

        return ast.FunctionCall(ident, args)

    def parse_block(self):
        if not isinstance(self.current, tokens.LBRACE):
            raise ParserError(f"Expected {'{'} after function, found `{self.current}`")
        self.step()
        statements = []
        while not isinstance(self.current, tokens.EOF):
            if isinstance(self.current, tokens.SEMICOLON):
                self.step()
                continue
            if isinstance(self.current, tokens.LET):
                stmt = self.parse_let()
            elif isinstance(self.current, tokens.FUNC):
                stmt = self.parse_function_literal()
            elif isinstance(self.current, tokens.RETURN):
                stmt = self.parse_return()
            elif isinstance(self.current, tokens.IF):
                stmt = self.parse_conditional()
            elif isinstance(self.current, tokens.LBRACE):
                stmt = self.parse_block()
            elif isinstance(self.current, tokens.RBRACE):
                break
            else:
                stmt = self.parse_expr()

            statements.append(stmt)
        
        self.step()
        
        return ast.Block(statements)

    def parse_function_literal(self):
        self.step()
        if not isinstance(self.current, tokens.LPARAN):
            raise ParserError(f"Expected `(` after function name, found {self.current}")
        
        if isinstance(self.read_char(), tokens.RPARAN):
            return ast.FunctionCall(ident, [])

        params = []
        while True:
            if isinstance(self.current, tokens.RPARAN):
                break
            params.append(self.parse_expr())

            if isinstance(self.current, tokens.COMMA):
                self.step()

        self.step()

        body = self.parse_block()

        return ast.FunctionLiteral(params, body)

    def parse_expr(self):
        self.step_back()
        expr = self.expr()
        self.step()

        return expr

    def expr(self, rbp=0):
        left = self.nud(self.read_char())
        while self.bp(self.next) > rbp:
            left = self.led(left, self.read_char())
        
        return left

    def bp(self, token):
        op = token.literal
        if op in {'==', '!='}:
            return 20
        if op in {'>', '<', '<=', '>='}:
            return 40
        if op in {'+', '-'}:
            return 50
        if op in {'*', '/'}:
            return 60
        
        return 0

    def nud(self, token):
        if isinstance(token, tokens.IDENT):
            if isinstance(self.next, tokens.LPARAN):
                return self.parse_function_call()
            else:
                return ast.Identifier(token)
        if isinstance(token, tokens.INT):
            return ast.IntLiteral(token)
        if isinstance(token, tokens.FUNC):
            func = self.parse_function_literal()
            self.step_back()
            return func
        if isinstance(token, (tokens.TRUE, tokens.FALSE)):
            return ast.BoolLiteral(token)
        if isinstance(token, tokens.MINUS):
            return ast.PrefixOp(token, self.nud(self.read_char()))
        else:
            raise ParserError(f"No prefix parse function found for {token}")

    
    def led(self, left, token):
        if isinstance(token, (tokens.PLUS, tokens.MINUS, tokens.ASTERISK, tokens.SLASH)):
            return ast.BinaryOp(token, left , self.expr(self.bp(token)))
        if isinstance(token, (tokens.EQ, tokens.NEQ, tokens.LT, tokens.GT, tokens.LTE, tokens.GTE)):
            return ast.BinaryOp(token, left, self.expr(self.bp(token)))
        else:
            raise ParserError(f"No infix parse function found for {token}")

def parse(tokens):
    p = Parser(tokens)
    return p.parse_program()

def parse_source(source):
    from lexer import tokenize
    toks = tokenize(source)

    p = Parser(toks)

    return p.parse_program()
