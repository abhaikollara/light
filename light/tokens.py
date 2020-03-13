class Token:
    def __init__(self, literal):
        self.literal = literal

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self.literal})"


class ILLEGAL(Token):
    def __init__(self, literal):
        self.literal = literal

class EOF(Token):
    def __init__(self):
        self.literal = '\0'

class IDENT(Token):
    def __init__(self, literal):
        self.literal = literal

class ASSIGN(Token):
    def __init__(self):
        self.literal = '='

class COMMA(Token):
    def __init__(self):
        self.literal = ','

class SEMICOLON(Token):
    def __init__(self):
        self.literal = ';'

class INT(Token):
    def __init__(self, literal):
        self.literal = literal

#
# Keywords
#

class IF(Token):
    def __init__(self):
        self.literal = 'if'

class ELSE(Token):
    def __init__(self):
        self.literal = 'else'

class LET(Token):
    def __init__(self):
        self.literal = 'let'

class FUNC(Token):
    def __init__(self):
        self.literal = 'func'

class RETURN(Token):
    def __init__(self):
        self.literal = 'return'

#
# Brackets
#

class LPARAN(Token):
    def __init__(self):
        self.literal = '('

class RPARAN(Token):
    def __init__(self):
        self.literal = ')'

class LBRACE(Token):
    def __init__(self):
        self.literal = '{'

class RBRACE(Token):
    def __init__(self):
        self.literal = '}'

#
# Boolean Literals
#

class TRUE(Token):
    def __init__(self):
        self.literal = 'true'

class FALSE(Token):
    def __init__(self):
        self.literal = 'false'

#
# Arithmetic Ops
#

class PLUS(Token):
    def __init__(self):
        self.literal = '+'

class MINUS(Token):
    def __init__(self):
        self.literal = '-'

class ASTERISK(Token):
    def __init__(self):
        self.literal = '*'

class SLASH(Token):
    def __init__(self):
        self.literal = '/'

#
# Relational Ops
#

class EQ(Token):
    def __init__(self):
        self.literal = '=='

class NEQ(Token):
    def __init__(self):
        self.literal = '!='

class GT(Token):
    def __init__(self):
        self.literal = '>'

class LT(Token):
    def __init__(self):
        self.literal = '<'

class GTE(Token):
    def __init__(self):
        self.literal = '>='

class LTE(Token):
    def __init__(self):
        self.literal = '<='