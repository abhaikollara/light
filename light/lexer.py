import string
import tokens

class LexerError(Exception):
    pass

KEYWORDS = {
    'if': tokens.IF,
    'else': tokens.ELSE,
    'let': tokens.LET,
    'func': tokens.FUNC,
    'return': tokens.RETURN,
    'true': tokens.TRUE,
    'false': tokens.FALSE,
}

SINGLE_CHAR_TOKENS = {
    '\0': tokens.EOF,
    '=': tokens.ASSIGN,
    '+': tokens.PLUS,
    '-': tokens.MINUS,
    '*': tokens.ASTERISK,
    '/': tokens.SLASH,
    '}': tokens.RBRACE,
    '{': tokens.LBRACE,
    ')': tokens.RPARAN,
    '(': tokens.LPARAN,
    ',': tokens.COMMA,
    ';': tokens.SEMICOLON,
    '<': tokens.LT,
    '>': tokens.GT,
}

DOUBLE_CHAR_TOKENS = {
    '==': tokens.EQ,
    '!=': tokens.NEQ,
    '>=': tokens.GTE,
    '<=': tokens.LTE,
}

class Lexer:

    def __init__(self, source):
        self.source = source
        self.position = 0
    
    @property
    def current_char(self):
        try:
            return self.source[self.position]
        except IndexError:
            return '\0'

    @property
    def next_char(self):
        try:
            return self.source[self.position+1]
        except IndexError:
            return '\0'

    def step(self, n=1):
        self.position += n

    def skip_whitespace(self):
        while self.current_char in string.whitespace:
            self.step()

    def read_string(self):
        pos = self.position
        while self.next_char in string.ascii_letters+'_':
            self.step()
        
        return self.source[pos:self.position+1]
    
    def read_number(self):
        pos = self.position
        try:
            while self.next_char in string.digits:
                self.step()
        except LexerError:
            pass
        
        return self.source[pos:self.position+1]

    def next_token(self):
        self.skip_whitespace()
        
        if self.current_char+self.next_char in DOUBLE_CHAR_TOKENS:
            token = DOUBLE_CHAR_TOKENS[self.current_char+self.next_char]()
            self.step()

        elif self.current_char in SINGLE_CHAR_TOKENS:
            token = SINGLE_CHAR_TOKENS[self.current_char]()

        elif self.current_char in string.digits:
            num = self.read_number()
            token = tokens.INT(num)
        
        elif self.current_char in string.ascii_letters + '_':
            string_ = self.read_string()
            if string_ in KEYWORDS:
                token = KEYWORDS[string_]()
            else:
                token = tokens.IDENT(string_)
        else:
            token = tokens.ILLEGAL(self.current_char)

        self.step()

        return token

    def scan(self):
        toks = []

        while True:
            t = self.next_token()
            toks.append(t)
            if isinstance(t, tokens.EOF):
                break
        
        return toks

def tokenize(source):
    l = Lexer(source)

    return l.scan()